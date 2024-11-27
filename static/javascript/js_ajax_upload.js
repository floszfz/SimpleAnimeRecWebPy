/*
 * 自定义公共jquery.ajax异步上传文件js方法
 */

/**
 * 图片上传
 *
 * @param requestUrl
 *            上传地址
 * @param id
 *            文件id
 * @param paramDatas
 *            其他参数（json格式）
 */
function jqueryAjaxUploadImageFun(requestUrl, id, paramDatas) {
    var fileid = "#" + id + "_file";// 上传文件框id
    var imageid = "#" + id + "_image";// 回显图片id
    var hiddenid = "#" + id;// 隐藏域id
    // 文件对象
    var file = $(fileid)[0].files[0];
    // 文件大小，单位B字节
    var fileSize = file.size;

    // 最大上传文件大小，10MB
    var maxFileSize = 1024 * 1024 * 10;

    // 文件大小判断
    if (fileSize > maxFileSize) {
        $(fileid).val("");// 清空选择的文件
        layer.msg("无效图片！大小10MB以内！");
        return false;
    }

    // 创建一个表单对象
    var formData = new FormData();
    // 表单中添加文件数据
    formData.append("file", file);
    // 表单中添加其他参数
    for (var paramDataKey in paramDatas) {
        formData.append(paramDataKey, paramDatas[paramDataKey]);
    }

    // jquery.ajax提交表单
    $.ajax({
        contentType: "multipart/form-data",// 文件传输为二进制类型
        url: baseUrl + requestUrl,// 上传地址
        type: "post",// 请求方式
        data: formData,// 请求数据
        dataType: "json",// 返回数据类型
        processData: false, // 不去处理发送的数据（jquery不序列化数据）
        contentType: false, // 不去设置Content-Type请求头
        success: function (returnData) {
            if (returnData.success > 0) {// 上传成功
                // 修改文件隐藏域值为文件名字，最终这个文件名字会保存在数据库
                $(hiddenid).val(returnData.newFileName);
                // 显示选中的图片
                $(imageid).attr("src", baseUploadUrl + returnData.newFileName);
                $(imageid).css("display", "block");
                // 提示信息
                if (returnData.message != null && returnData.message != "") {
                    // 后端返回的上传成功提示信息
                    layer.msg(returnData.message);
                } else {
                    layer.msg("上传成功！");
                }
            } else {
                // 上传失败
                if (returnData.message != null && returnData.message != "") {
                    // 后端返回的上传失败提示信息
                    layer.msg(returnData.message);
                } else {
                    layer.msg("上传失败！");
                }
            }
        },
        error: function (returnData) {
            console.info("jquery ajax upload file error...");
            layer.msg("上传失败！");
        }
    });

}