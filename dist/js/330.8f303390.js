"use strict";(self["webpackChunkmyweb"]=self["webpackChunkmyweb"]||[]).push([[330],{3292:function(e,a,l){l.r(a),l.d(a,{default:function(){return f}});var o=l(3396),t=l(9242);const n={style:{"margin-bottom":"5px"}},r={class:"dialog-footer"};function i(e,a,l,i,m,u){const d=(0,o.up)("el-input"),s=(0,o.up)("el-button"),p=(0,o.up)("el-table-column"),c=(0,o.up)("el-popconfirm"),f=(0,o.up)("el-table"),g=(0,o.up)("el-pagination"),h=(0,o.up)("el-col"),b=(0,o.up)("el-form-item"),k=(0,o.up)("el-form"),w=(0,o.up)("el-dialog");return(0,o.wg)(),(0,o.iD)("div",null,[(0,o._)("div",n,[(0,o.Wm)(d,{modelValue:e.name,"onUpdate:modelValue":a[0]||(a[0]=a=>e.name=a),modelModifiers:{trim:!0},placeholder:"请输入分类名","suffix-icon":i.ElIconSearch,style:{width:"200px"},onKeyup:(0,t.D2)(i.loadPost,["enter"])},null,8,["modelValue","suffix-icon","onKeyup"]),(0,o.Wm)(s,{type:"primary",style:{"margin-left":"5px"},onClick:i.loadPost},{default:(0,o.w5)((()=>[(0,o.Uk)("查询")])),_:1},8,["onClick"]),(0,o.Wm)(s,{type:"success",onClick:i.resetParam},{default:(0,o.w5)((()=>[(0,o.Uk)("重置")])),_:1},8,["onClick"]),(0,o.Wm)(s,{type:"primary",style:{"margin-left":"5px"},onClick:i.add},{default:(0,o.w5)((()=>[(0,o.Uk)("新增")])),_:1},8,["onClick"])]),(0,o.Wm)(f,{data:e.tableData,"header-cell-style":{background:"#f2f5fc",color:"#555555"},border:""},{default:(0,o.w5)((()=>[(0,o.Wm)(p,{prop:"id",label:"ID",width:"60"}),(0,o.Wm)(p,{prop:"name",label:"分类名",width:"180"}),(0,o.Wm)(p,{prop:"remark",label:"备注"}),(0,o.Wm)(p,{prop:"operate",label:"操作"},{default:(0,o.w5)((e=>[(0,o.Wm)(s,{size:"small",type:"success",onClick:a=>i.mod(e.row)},{default:(0,o.w5)((()=>[(0,o.Uk)("编辑")])),_:2},1032,["onClick"]),(0,o.Wm)(c,{title:"确定删除吗？",onConfirm:a=>i.del(e.row.id),style:{"margin-left":"5px"}},{reference:(0,o.w5)((()=>[(0,o.Wm)(s,{size:"small",type:"danger"},{default:(0,o.w5)((()=>[(0,o.Uk)("删除")])),_:1})])),_:2},1032,["onConfirm"])])),_:1})])),_:1},8,["data"]),(0,o.Wm)(g,{onSizeChange:i.handleSizeChange,onCurrentChange:i.handleCurrentChange,"current-page":e.pageNum,"page-sizes":[5,10,20,30],"page-size":e.pageSize,layout:"total, sizes, prev, pager, next, jumper",total:e.total},null,8,["onSizeChange","onCurrentChange","current-page","page-size","total"]),(0,o.Wm)(w,{title:"提示",modelValue:e.centerDialogVisible,"onUpdate:modelValue":a[4]||(a[4]=a=>e.centerDialogVisible=a),width:"30%",center:""},{footer:(0,o.w5)((()=>[(0,o._)("span",r,[(0,o.Wm)(s,{onClick:a[3]||(a[3]=a=>e.centerDialogVisible=!1)},{default:(0,o.w5)((()=>[(0,o.Uk)("取 消")])),_:1}),(0,o.Wm)(s,{type:"primary",onClick:i.save},{default:(0,o.w5)((()=>[(0,o.Uk)("确 定")])),_:1},8,["onClick"])])])),default:(0,o.w5)((()=>[(0,o.Wm)(k,{ref:"forms",rules:e.rules,model:e.form,"label-width":"80px"},{default:(0,o.w5)((()=>[(0,o.Wm)(b,{label:"分类名",prop:"name"},{default:(0,o.w5)((()=>[(0,o.Wm)(h,{span:20},{default:(0,o.w5)((()=>[(0,o.Wm)(d,{modelValue:e.form.name,"onUpdate:modelValue":a[1]||(a[1]=a=>e.form.name=a),modelModifiers:{trim:!0}},null,8,["modelValue"])])),_:1})])),_:1}),(0,o.Wm)(b,{label:"备注",prop:"remark"},{default:(0,o.w5)((()=>[(0,o.Wm)(h,{span:20},{default:(0,o.w5)((()=>[(0,o.Wm)(d,{type:"textarea",modelValue:e.form.remark,"onUpdate:modelValue":a[2]||(a[2]=a=>e.form.remark=a),modelModifiers:{trim:!0}},null,8,["modelValue"])])),_:1})])),_:1})])),_:1},8,["rules","model"])])),_:1},8,["modelValue"])])}var m=l(4870),u=l(7178),d=l(2748),s={setup(){const e=(0,o.f3)("axios"),a=(0,m.qj)({tableData:[],pageSize:10,pageNum:1,total:0,name:"",centerDialogVisible:!1,form:{id:"",name:"",remark:""},rules:{name:[{required:!0,message:"请输入分类名",trigger:"blur"}]}});function l(){Object.keys(a.form).forEach((e=>{a.form[e]=""}))}function t(a){console.log(a),e.get("/goodstype/del?id="+a).then((e=>e.data)).then((e=>{console.log(e),200==e.code?(u.z8.success("操作成功！"),b()):u.z8.error("操作失败！")}))}function n(e){console.log(e),a.centerDialogVisible=!0,(0,o.Y3)((()=>{a.form.id=e.id,a.form.name=e.name,a.form.remark=e.remark}))}function r(){a.centerDialogVisible=!0,(0,o.Y3)((()=>{l()}))}function i(){e.post("/goodstype/save",a.form).then((e=>e.data)).then((e=>{console.log(e),200==e.code?(u.z8.success("操作成功！"),a.centerDialogVisible=!1,b(),l()):u.z8.error("操作失败！")}))}function s(){e.post("/goodstype/update",a.form).then((e=>e.data)).then((e=>{console.log(e),200==e.code?(u.z8.success("操作成功！"),a.centerDialogVisible=!1,b(),l()):u.z8.error("操作失败！")}))}const p=(0,m.iH)(null);function c(){p.value.validate((e=>{if(!e)return console.log("error submit!!"),!1;a.form.id?s():i()}))}function f(e){console.log(`每页 ${e} 条`),a.pageNum=1,a.pageSize=e,b()}function g(e){console.log(`当前页: ${e}`),a.pageNum=e,b()}function h(){a.name=""}function b(){e.post("/goodstype/listPage",{pageSize:a.pageSize,pageNum:a.pageNum,param:{name:a.name}}).then((e=>e.data)).then((e=>{200==e.code?(a.tableData=e.data,a.total=e.total):alert("获取数据失败")}))}return(0,o.wF)((()=>{b()})),{...(0,m.BK)(a),ElIconSearch:d.Search,forms:p,del:t,mod:n,add:r,save:c,handleCurrentChange:g,handleSizeChange:f,resetParam:h,loadPost:b}},name:"GoodstypeManage"},p=l(89);const c=(0,p.Z)(s,[["render",i]]);var f=c}}]);
//# sourceMappingURL=330.8f303390.js.map