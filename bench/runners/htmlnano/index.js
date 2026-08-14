const htmlnano = require("htmlnano");
const { htmlOnly, run } = require("../common");

const options = htmlOnly
  ? { minifyCss: false, minifyJs: false, minifyJson: false, minifySvg: false }
  : { minifyCss: false, minifySvg: false };

run((src) => htmlnano.process(src.toString(), options).then((r) => r.html));
