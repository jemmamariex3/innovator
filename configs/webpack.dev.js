// Webpack uses this to work with directories
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin'); 
const CopyWebpackPlugin = require('copy-webpack-plugin'); 

const srcDir = path.resolve(__dirname, '..', 'src'); 
const distDir = path.resolve(__dirname, '..', 'dist'); 

const htmlPlugin = new HtmlWebpackPlugin({
  path: distDir, 
  filename: 'index.html', 
  template: path.join(srcDir, '..', 'index.html'), 
}); 
const copyPlugin = new CopyWebpackPlugin([
  { from: path.join(srcDir, 'assets'), to: 'assets' }
])

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

  // Default mode for Webpack is production.
  // Depending on mode Webpack will apply different things
  // on final bundle. For now we don't need production's JavaScript
  // minifying and other thing so let's set mode to development
  mode: 'development', 

  devServer: {
    contentBase: srcDir, 
    publicPath: '/', 
    historyApiFallback: true, 
    port: 8000, 
  }, 

  module: {
    rules: [
      {
        test: /\.css$/, 
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
  
  plugins: [htmlPlugin, copyPlugin]
};
