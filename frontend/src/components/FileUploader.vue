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
      >
    </div>
    <div
      class="card card-footer"
      v-if="filepath && (fileTooLarge || !uploadOnFocusOut)"
    >
      <div class="progress" v-if="loading">
        <div
          class="progress-bar"
          role="progressbar"
          :style="{ width: uploadpercent }"
          aria-valuenow="0"
          aria-valuemin="0"
          aria-valuemax="100"
        ></div>
      </div>
      <button
        :disabled="fileTooLarge"
        v-else-if="fileTooLarge || !uploadOnFocusOut"
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
  components: {}
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
  // private uploadPercentage = 0;
  // private uploadInfo: UploadInfo = {
  //   started: new Date(),
//   transferred: 0,
//   toTransfer: 0
// };

  setFilePath(event) {
    this.filepath = event.target.files[0];
  }

  // get uploadpercent() {
  //   if (!(this.uploadInfo.transferred && this.uploadInfo.toTransfer)) {
  //     return "0";
  //   } else {
  //     return (
  //       ((100 * this.uploadInfo.transferred) / this.uploadInfo.toTransfer)
  //       .toFixed(0)
  //       .toString() + "%"
  //     );
  //   }
  // }

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
    // this.uploadInfo = {
    //   started: new Date(),
//   transferred: NaN,
//   toTransfer: NaN
// };
// 
// const updateUploadPercentage = evt => {
//   this.uploadInfo.transferred = evt.loaded;
//   this.uploadInfo.toTransfer = evt.total;
//   this.$emit("progress", this.uploadInfo);
// };

    if (this.filepath && this.endpoint) {
      this.loading = true;
      this.$emit("uploadStarted");

      console.log(this.filepath);

      const formData = this.formData;

      axios
      .post(this.endpoint, formData, {
        // onUploadProgress: updateUploadPercentage
      })
      .then(ans => {
        this.$emit("uploadFinished", ans.data);
        this.$emit("input", ans.data);
        this.loading = false;
        this.uploaded = true;
      })
      .catch(err => {
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
