<template>
  <div>
    <div class="mb-3">
      <label for="formFile" class="form-label" v-if="placeholder">{{
        placeholder
      }}</label>
      <input
        type="file"
        class="form-control"
        id="formFile"
        @change="setFilePath"
        :state="undefined"
        :placeholder="placeholder"
        :drop-placeholder="placeholder"
      />
    </div>
    <div
      class="card card-footer"
      v-if="filepath && (fileTooLarge || !uploadOnFocusOut)"
    >
      <button
        :disabled="fileTooLarge"
        v-if="fileTooLarge || !uploadOnFocusOut"
        class="btn btn-primary"
        @click="upload"
      >
        {{
          !fileTooLarge
            ? uploadButtonText
            : "Le fichier est trop volumineux! Taille maximum: " +
              (maxSize / 1e6).toFixed(0) +
              "Mo"
        }}
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from "vue-property-decorator";
import axios from "axios";
// import { UploadInfo } from "@/types";

axios.defaults.baseURL = process.env.BASE_URL;

@Component({
  components: {},
})
export default class FileUploader extends Vue {
  private filepath: File | null = null;

  @Prop({ default: undefined })
  value!: any | undefined;

  @Prop()
  private endpoint: string | undefined;

  @Prop({ default: "envoyer" })
  private uploadButtonText: string | undefined;

  @Prop({ default: 10e6 })
  private maxSize: number | undefined;

  @Prop({ default: "Select a file..." })
  private placeholder: string | undefined;

  @Prop({ default: false })
  private uploadOnFocusOut: boolean | undefined;

  fileTooLarge = false;

  private loading = false;
  private uploaded = false;

  setFilePath(event) {
    this.filepath = event.target.files[0];
  }

  get formData() {
    if (this.filepath) {
      const f = new FormData();
      f.append(this.filepath.name, this.filepath);
      console.log("formdata:");
      console.log(f);
      console.log(this.filepath);
      return f;
    } else {
      return null;
    }
  }

  get formDataSize() {
    return this.formData ? ([...this.formData.entries()][0][1] as any).size : 0;
  }

  get fileSizeOk() {
    return (
      !this.maxSize || !~this.maxSize || this.formDataSize <= this.maxSize * 1e6
    );
  }

  private upload() {
    if (this.filepath && this.endpoint) {
      this.loading = true;
      this.$emit("uploadStarted");

      console.log(this.filepath);

      const formData = this.formData;

      axios
        .post(this.endpoint, formData, {
        })
        .then((ans) => {
          this.$emit("uploadFinished", ans.data);
          this.$emit("input", ans.data);
          this.loading = false;
          this.uploaded = true;
        })
        .catch((err) => {
          console.log(err);
          this.$emit("uploadError", err.response.data);
          // this.$toast.error(err.response.data);
          this.loading = false;
        });
    }
  }

  @Watch("filepath")
  filepathChanged() {
    if (this.formData && this.maxSize) {
      const sz = this.formDataSize;
      console.log("ok");
      console.log(this.maxSize);
      console.log(sz);
      if (~this.maxSize && sz > this.maxSize) {
        this.fileTooLarge = true;
      } else {
        this.fileTooLarge = false;
        if (this.uploadOnFocusOut) {
          this.upload();
        }
      }
    }
  }
}
</script>

<style>
.custom-file-input.is-invalid ~ .custom-file-label {
  border-color: white !important;
}
</style>
