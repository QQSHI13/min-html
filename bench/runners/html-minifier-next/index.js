const { minify } = require("html-minifier-next");
const { htmlOnly, esbuildCss, esbuildJs, run } = require("../common");

const htmlMinifierCfg = {
  collapseBooleanAttributes: true,
  collapseInlineTagWhitespace: true,
  collapseWhitespace: true,
  // min-html can do context-aware whitespace removal, which is safe when configured correctly to match how whitespace is used in the document.
  // html-minifier-next cannot, so whitespace must be collapsed conservatively.
  // Alternatively, min-html can also be made to remove whitespace regardless of context.
  conservativeCollapse: true,
  customEventAttributes: [],
  decodeEntities: true,
  ignoreCustomComments: [],
  ignoreCustomFragments: [/<\?[\s\S]*?\?>/],
  minifyCSS: !htmlOnly && esbuildCss,
  minifyJS: !htmlOnly && esbuildJs,
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
