const { minify } = require("html-minifier-terser");
const { htmlOnly, esbuildCss, esbuildJs, run } = require("../common");

const htmlMinifierCfg = {
  collapseBooleanAttributes: true,
  collapseInlineTagWhitespace: true,
  collapseWhitespace: true,
  conservativeCollapse: true,
  customEventAttributes: [],
  decodeEntities: true,
  ignoreCustomComments: [],
  ignoreCustomFragments: [/<\?[\s\S]*?\?>/],
  minifyCSS: !htmlOnly && ((code, type) => Promise.resolve(esbuildCss(code, type))),
  minifyJS: !htmlOnly && ((code) => Promise.resolve(esbuildJs(code))),
  processConditionalComments: true,
  removeAttributeQuotes: true,
  removeComments: true,
  removeEmptyAttributes: true,
  removeOptionalTags: true,
  removeRedundantAttributes: true,
  removeScriptTypeAttributes: true,
  removeStyleLinkTypeAttributes: true,
  removeTagWhitespace: true,
  useShortDoctype: true,
};

run((src) => minify(src.toString(), htmlMinifierCfg));
