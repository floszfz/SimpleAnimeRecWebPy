/*
 * 自定义公共jquery.ajax异步提交数据js方法
 * 使用jquery.ajax异步提交数据的技术，并封装了请求地址、请求参数、返回结果处理
 */

var jqueryAjaxTimeout = 800;// 设置jquery.ajax请求后跳转页面的时间间隔

/**
 * 定义jquery.ajax提交数据的方法
 * 
 * @param requestUrl
 *            请求地址
 * @param requestData
 *            请求数据
 */
function jqueryAjaxFun(requestUrl, requestData) {
	// jquery.ajax异步请求参数
	var options = {
		url : baseUrl + requestUrl,// 请求地址
		type : 'post',// 请求方式post或者get
		dataType : 'json',// 后端返回的数据类型，json格式
		data : requestData,// 请求参数
		success : function(returnData) {// 接收后端返回的数据
			if (returnData.success > 0) {// 操作成功
				if (returnData.message != null && returnData.message != "") {
					// 后端返回的操作成功提示信息
					layer.msg(returnData.message);
				} else {
					layer.msg("操作成功！");
				}
				// 如果后端返回的有跳转的url，那么跳转
				if (returnData.toUrl != null && returnData.toUrl != "") {
					// 刷新当前页面
					if (returnData.toUrl == "reload") {
						setTimeout(function() {
							window.location.reload();
						}, jqueryAjaxTimeout);
					} else {
						// 跳转到后端指定的url
						setTimeout(function() {
							location.href = baseUrl + returnData.toUrl;
						}, jqueryAjaxTimeout);
					}
				}
			} else {
				// 操作失败
				if (returnData.message != null && returnData.message != "") {
					// 后端返回的操作失败提示信息
					layer.msg(returnData.message);
				} else {
					layer.msg("操作失败！");
				}
			}
		},
		error : function(returnData) {// 后端服务器异常处理（代码报错等错误）
			jqueryAjaxErrorFun(returnData, requestUrl);
		}
	};
	// jquery.ajax异步提交请求
	$.ajax(options);
}

/**
 * 定义jquery.ajax提交数据的方法，请求之后，有父级页面负责跳转页面
 * 
 * @param requestUrl
 *            请求地址
 * @param requestData
 *            请求数据
 */
function jqueryAjaxIframeFun(requestUrl, requestData) {
	// jquery.ajax异步请求参数
	var options = {
		url : baseUrl + requestUrl,// 请求地址
		type : 'post',// 请求方式post或者get
		dataType : 'json',// 后端返回的数据类型，json格式
		data : requestData,// 请求参数
		success : function(returnData) {// 接收后端返回的数据
			if (returnData.success > 0) {// 操作成功
				if (returnData.message != null && returnData.message != "") {
					// 后端返回的操作成功提示信息
					layer.msg(returnData.message);
				} else {
					layer.msg("操作成功！");
				}
				// 如果后端返回的有跳转的url，那么跳转
				if (returnData.toUrl != null && returnData.toUrl != "") {
					// 刷新当前页面
					if (returnData.toUrl == "reload") {
						setTimeout(function() {
							parent.window.location.reload();
						}, jqueryAjaxTimeout);
					} else {
						// 跳转到后端指定的url
						setTimeout(function() {
							parent.location.href = baseUrl + returnData.toUrl;
						}, jqueryAjaxTimeout);
					}
				}
			} else {
				// 操作失败
				if (returnData.message != null && returnData.message != "") {
					// 后端返回的操作失败提示信息
					layer.msg(returnData.message);
				} else {
					layer.msg("操作失败！");
				}
			}
		},
		error : function(returnData) {// 后端服务器异常处理（代码报错等错误）
			jqueryAjaxErrorFun(returnData, requestUrl);
		}
	};
	// jquery.ajax异步提交请求
	$.ajax(options);
}

/**
 * 定义jquery.ajax提交数据的方法，回调函数自己处理后端返回结果
 * 
 * @param requestUrl
 *            请求地址
 * @param requestData
 *            请求数据
 * @param callbackFun
 *            回调函数
 */
function jqueryAjaxCallbackFun(requestUrl, requestData, callbackFun) {
	// jquery.ajax异步请求参数
	var options = {
		url : baseUrl + requestUrl,
		type : 'post',
		dataType : 'json',
		data : requestData,
		success : function(returnData) {
			// 调用回调函数，处理后端返回结果
			if (callbackFun != null) {
				callbackFun(returnData);
			}
		},
		error : function(returnData) {// 后端服务器异常处理（代码报错等错误）
			jqueryAjaxErrorFun(returnData, requestUrl);
		}
	};
	// jquery.ajax异步提交请求
	$.ajax(options);
}

/**
 * 定义jquery.ajax提交数据后，后端代码异常的处理方法
 * 
 * @param returnData
 *            返回数据
 * @param requestUrl
 *            请求地址
 */
function jqueryAjaxErrorFun(returnData, requestUrl) {
	console.info("jquery ajax error...");
	if (returnData.status == 403) {
		layer.msg("操作失败，请先登录！");
	} else {
		console.info(returnData.responseText);
		layer.msg("操作失败，服务器异常！");
	}
}
