const fs = require("fs");
const path = require("path");

const inputDir = path.join(__dirname, "inputs");

// Large synthetic HTML with lots of minifiable content.
const synthetic = (name, body) => {
  const html = `<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>${name}</title>
    <!-- This is a comment that minifiers can remove -->
    <style type="text/css">
      /* CSS comment */
      body {
        color: #ff0000;
        margin: 0px 0px 0px 0px;
      }
    </style>
  </head>
  <body>
    ${body}
    <script type="text/javascript">
      // JS comment
      var x = 1 + 2;
    </script>
  </body>
</html>`;
  fs.writeFileSync(path.join(inputDir, name), html);
};

// Input 1: lots of whitespace and comments.
synthetic(
  "Synthetic-Whitespace",
  Array(1000)
    .fill(`<div class="container">
      <p>Hello world</p>
      <!-- inline comment -->
      <span>foo</span>
    </div>`)
    .join("\n")
);

// Input 2: redundant/empty attributes and optional tags.
synthetic(
  "Synthetic-Redundant",
  Array(1000)
    .fill(`<div class="item" id="id" style="">
      <input type="text" value="">
      <br />
      <p></p>
    </div>`)
    .join("\n")
);

// Input 3: repeated inline CSS and JS.
const repeatedBlock = `<div style="color: #0000ff; background-color: #ffffff; ">
      <span onclick="alert('hello');">click</span>
    </div>`;
synthetic("Synthetic-Inline", Array(1000).fill(repeatedBlock).join("\n"));

console.log("Generated synthetic unminified inputs.");
