//vue.config.js
module.exports = {
    publicPath: './',
    runtimeCompiler: true,
    devServer: {
        host: 'localhost', //target host
        port: 5005,
        proxy: {
            '/testcase': {
                target: 'http://127.0.0.1:5000',
                ws: true,
                changeOrigin: true,
                pathRewrite: {
                    '^/testcase': '/test_case'
                        //pathRewrite: {'^/api': '/'} 重写之后url为 http://192.168.1.16:8085/xxxx
                        //pathRewrite: {'^/api': '/api'} 重写之后url为 http://192.168.1.16:8085/api/xxxx
                }
            },

        }
    }
}