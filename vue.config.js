const HtmlWebpackInlineSourcePlugin = require('html-webpack-inline-source-plugin');
module.exports = {
    chainWebpack: config => {
        if (process.env.NODE_ENV === 'production') {
            config.plugin('html-inline').use(HtmlWebpackInlineSourcePlugin);
            config.plugin('html').tap(args => {
                args[0].inlineSource = '.(js|css)$'
                return args
            })
        }
    }
}
