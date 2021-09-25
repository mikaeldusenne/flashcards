module.exports = {
  publicPath: ((e) => (e.startsWith("/") ? e : "/" + e))(
    "/mikarezoo-flashcards"
  ),
  assetsDir: "./static",
  outputDir: "./dist/",
  devServer: {
    proxy: "http://mikarezoo-flashcards_app:5000",
  },
    lintOnSave: true,
};
