# actions

## 如何配置

actions 需要创建gpts， 然后配置 `指令` 和 `actions`

- 指令： 一段描述，来说明如何触发这个action
- actions： 一个json对象，定义了action的输入和输出

- [actions 配置](https://platform.openai.com/docs/guides/actions/create-actions)
- [官网的简单使用](https://platform.openai.com/docs/actions/getting-started)
- [smolex ChatGPT 的代码实体检索“GPT action”](https://github.com/loladotdev/smolex)
   - 先把代码转成ast信息存入数据库， 写一个查询接口，查到ast信息后， 转成function call 的参数。
- 


总结： actions 就是 function call 的封装， 没必要非要去配置actions， 直接使用 function call 即可。

> 花了挺长时间的，目前感觉在编程过程中用处不大
