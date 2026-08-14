const { minify } = require("@swc/html");
const { htmlOnly, run } = require("../common");

const options = {
  collapseWhitespaces: "smart",
  removeComments: true,
  removeEmptyAttributes: true,
  removeRedundantAttributes: "all",
  collapseBooleanAttributes: true,
  minifyCss: !htmlOnly,
  minifyJs: !htmlOnly,
  minifyJson: !htmlOnly,
  quotes: true,
  tagOmission: false,
};

run((src) => minify(src.toString(), options).then((r) => r.code));
