$(document).ready(function(){
    // 点击关键词检索按钮，发请求
    $("#btn-submit2search").on("click", function () {
        var keyword = $.trim($('input[name="submit2search"]').val());
        if (keyword === "")
            return;
        $.ajax({
            method: "GET",
            url: "/keysearch",
            data: {
                "id": $("#submit2search").attr("id"),
                "keyword": keyword
            },
            dataType: "json",
            beforeSend: function() {
                // 设置disabled阻止用户继续点击
                $("#btn-submit2search").attr("disabled", true);
            },
            complete: function () {
                // 请求完成移除 disabled 属性
                $("#btn-submit2search").removeAttr("disabled");
            },
            success: function(result){
                console.log(result);
                if(result.status === 200){
                    var data_list = result.text;
                    var data_oldlist = $("tr.data-entry");
                    if (data_oldlist && data_oldlist.length>0) {
                        // 清空原有表格
                        data_oldlist.remove();
                        $("ul.pagination").remove();
                    }
                    // 创建搜索结果的表格并插入到前端页面
                    for (var i = 0; i < data_list.length; i++) {
                        var search_html = i%2===0 ? '<tr class="table-primary data-entry">'
                        + '<td>' + data_list[i].publisher + '</td>'
                        + '<td>' + data_list[i].content + '</td>'
                        + '<td>' + data_list[i].number_of_comments + '</td>'
                        + '<td>' + data_list[i].number_of_likes + '</td>'
                        + '<td>' + data_list[i].number_of_shares + '</td>'
                        + '<td><a href="' + data_list[i].url + '">' + data_list[i].source_platform +'</a></td>'
                        + '</tr>' : '<tr class="table-secondary data-entry">'
                        + '<td>' + data_list[i].publisher + '</td>'
                        + '<td>' + data_list[i].content + '</td>'
                        + '<td>' + data_list[i].number_of_comments + '</td>'
                        + '<td>' + data_list[i].number_of_likes + '</td>'
                        + '<td>' + data_list[i].number_of_shares + '</td>'
                        + '<td><a href="' + data_list[i].url + '">' + data_list[i].source_platform +'</a></td>'
                        + '</tr>';
                        $("table#data-result-list-table").append($(search_html))
                    }
                    console.log("检索成功");
                    console.log(data_list);
                }else if(result.status === 201){
                    alert("检索不到任何结果!");
                }
                else{
                    alert("检索失败");
                }
            },
            error: function (jqXHR, textStatus, e) {
                alert("提交异常："+e);
            }
        });
    })

    $("#btn-text2search").on("click", function () {
        var text = $.trim($('input[name="text2search"]').val());
        if (text === "")
            return;
        window.location.href = "./search?text="+text;
    })
})
