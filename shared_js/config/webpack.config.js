const path = require('path');
const webpack = require('webpack');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');
const paths = require('./paths');

const config = {
  context: path.resolve(__dirname, '../../'),

  entry: paths.entry_points,

  output: {
    path: path.resolve('./ais_static/bundles/'),
    filename: "[name]-[hash].js",
  },

  watchOptions: {
    poll: 1000,
    ignored: /node_modules/
  },

  plugins: [
    new BundleTracker({
      path: path.resolve(__dirname, '../../'),
      filename: './webpack-stats.js'
    }),
    new CleanWebpackPlugin([path.resolve('./ais_static/bundles/')], {
      root: __dirname
    })
  ],

  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx'],
    modules: ['node_modules', 'shared_js']
  }
};

module.exports = config;
