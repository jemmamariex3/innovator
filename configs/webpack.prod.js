// Webpack uses this to work with directories
const path = require('path');
const htmlWebpackPlugin = require('html-webpack-plugin'); 

const srcDir = path.resolve(__dirname, '..', 'src'); 
const distDir = path.resolve(__dirname, '..', 'dist'); 
const htmlPlugin = new htmlWebpackPlugin({
  path: distDir, 
  filename: 'index.html', 
  template: path.join(srcDir, '..', 'index.html'), 
  minify: {
    html5: true, 
  }
}); 

// This is main configuration object.
// Here you write different options and tell Webpack what to do
module.exports = {
  // Path to your entry point. From this file Webpack will begin his work
  entry: path.join(srcDir, 'js', 'index.js'),

  // Path and filename of your result bundle.
  // Webpack will bundle all JavaScript into this file
  output: {
    path: distDir,
    filename: 'bundle.js'
  },

  mode: 'production',
  
  module: {
    rules: [
      {
        test: /\.css/, 
        exclude: /node_modules/, 
        use: [
          "style-loader", 
          "css-loader"
        ]
      }
    ]
  },

  resolve: {
    extensions: [".js"]
  }, 

  plugins: [htmlPlugin]
};
