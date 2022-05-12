const parser = require("@babel/parser");  // 解析，js转AST
const traverse = require("@babel/traverse").default;  // 转换
const t = require("@babel/types");
const generator = require("@babel/generator").default;  // 生成
 
const fs = require('fs');  // 文件读写
 
let encode_file = "./raw_js.js"

target_js = fs.readFileSync(encode_file, {encoding: "utf-8"});
 
// 尝试将该代码中的n都变为x
const visitor = {
    StringLiteral(path){
        let node = path.node
        delete node.extra

    }
}
 
let ast = parser.parse(target_js);
 
traverse(ast, visitor);
 
let {code} = generator(ast);

fs.writeFileSync("result.js", code)