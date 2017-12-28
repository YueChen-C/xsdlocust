/**
 * Created by TXCAP on 2017/10/20.
 */
function ShowElement(element) {
    var oldhtml = element.innerHTML;
    //创建新的input元素
    var newobj = document.createElement('input');
    //为新增元素添加类型
    newobj.type = 'text';
    //为新增元素添加value值
    newobj.value = oldhtml;
    //为新增元素添加光标离开事件
    newobj.onblur = function () {
        //当触发时判断新增元素值是否为空，为空则不修改，并返回原有值
        element.innerHTML = this.value == oldhtml ? oldhtml : this.value;
        //当触发时设置父节点的双击事件为ShowElement
        element.setAttribute("ondblclick", "ShowElement(this);");
    };
    //设置该标签的子节点为空
    element.innerHTML = '';
    //添加该标签的子节点，input对象
    element.appendChild(newobj);
    //设置选择文本的内容或设置光标位置（两个参数：start,end；start为开始位置，end为结束位置；如果开始位置和结束位置相同则就是光标位置）
    newobj.setSelectionRange(0, oldhtml.length);
    //设置获得光标
    newobj.focus();

    //设置父节点的双击事件为空
    newobj.parentNode.setAttribute("ondblclick", "");

}

function Openloader() {
    document.getElementById("loader-4").style.display = "block";
}


//页面取到选中的值
function check_black() {
    document.getElementById("loader-4").style.display = "block";
    var myForm = document.forms['form'];
    var blackName = document.getElementsByName("black");
    var keydataName = document.getElementsByName("keydata");
    var version = document.getElementsByName("version");
    var input = document.createElement('input');
    var Interfaceid = document.getElementsByName("Interfaceid");
    input.type = 'hidden';
    input.name = 'keydata';
    var myjson = {};

    for (var k = 0; k < keydataName.length; k++) {
        var mycars = [];
        if (blackName[k].checked == true) {
            mycars = [keydataName[k].innerText, version[k].innerText, 1];
        } else {
            mycars = [keydataName[k].innerText, version[k].innerText, 0];
        }
        myjson[Interfaceid[k].innerHTML] = mycars;
    }

    input.value = JSON.stringify(myjson);
    myForm.appendChild(input);
    myForm.submit();
}


//checkbox 全选/取消全选
var isCheckAll = false;
function swapCheck() {
    if (isCheckAll) {
        $("input[type='checkbox']").each(function () {
            this.checked = false;
        });
        isCheckAll = false;
    } else {
        $("input[type='checkbox']").each(function () {
            this.checked = true;
        });
        isCheckAll = true;
    }
}


function live_telecast() {


    var frequency = document.getElementById("frequency").value;
    var time = document.getElementById("time").value;
    var liveidlist = document.getElementsByName('liveid');
    if (!frequency) {
        var frequencygroup = document.getElementById('frequency-group');
        frequencygroup.setAttribute("class", "form-group has-error");
        return;
    } else if (!time) {
        var timegroup = document.getElementById('time-group');
        timegroup.setAttribute("class", "form-group has-error");
        return;
    }
    document.getElementById("loader-4").style.display = "block";

    var myjson = {};
    var myForm = document.forms['number'];
    var message = document.getElementsByName("message");
    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'data';
    myjson['frequency'] = frequency;
    myjson['time'] = time;

    var mycars = [];
    for (var k = 0; k < message.length; k++) {
        if (message[k].checked == true) {
            mycars.push(message[k].value)
        }
    }
    for (var i = 0; i < liveidlist.length; i++) {
        if (liveidlist[i].checked == true) {
            myjson['liveid'] = liveidlist[i].value;
        }
    }
    myjson['message'] = mycars;
    input.value = JSON.stringify(myjson);
    myForm.appendChild(input);
    myForm.submit();
}


function addInterface() {
    $("#Interfacename").val('');
    $("#Interfacjson").val('');
    $("#baocun").css('display', 'none');
    $("#tijiao").css('display', 'inline');
    $("#addInterface").modal("show");

}
function confirm(fun) {
    if ($("#myConfirm").length > 0) {
        $("#myConfirm").remove();
    }
    var html = "<div class='modal fade' id='myConfirm' >"
        + "<div class='modal-backdrop in' style='opacity:0; '></div>"
        + "<div class='modal-dialog' style='z-index:2901; margin-top:60px; width:400px; '>"
        + "<div class='modal-content'>"
        + "<div class='modal-header'  style='font-size:16px; '>"
        + "<span class='glyphicon glyphicon-envelope'>&nbsp;</span>信息！<button type='button' class='close' data-dismiss='modal'>"
        + "<span style='font-size:20px;  ' class='glyphicon glyphicon-remove'></span><tton></div>"
        + "<div class='modal-body text-center' id='myConfirmContent' style='font-size:18px; '>"
        + "是否确定要删除接口？"
        + "</div>"
        + "<div class='modal-footer ' style=''>"
        + "<button class='btn btn-danger ' id='confirmOk' >确定<tton>"
        + "<button class='btn btn-info ' data-dismiss='modal'>取消<tton>"
        + "</div>" + "</div></div></div>";
    $("body").append(html);

    var Interfaceid = document.getElementsByName("Interfaceid");
    var blackName = document.getElementsByName("black");
    var mycars = [];
    for (var k = 0; k < blackName.length; k++) {

        if (blackName[k].checked == true) {
            mycars.push(Interfaceid[k].innerText)
        }
    }

    if (mycars.length >=1) {
        $("#myConfirm").modal("show");
        $("#confirmOk").on("click", function () {
            $("#myConfirm").modal("hide");
            $.ajax({
                url: "/Deleteinterface",
                type: "POST",
                data: {"interface": mycars},
                cache: false,
                success: function (data) {
                    if (data['code'] == 0) {
                        location.reload();
                    } else {
                        alert(data['message'])
                    }

                }
            })
        });

    } else {
        alert("请选择接口")
    }


}

function Deleteinterface() {
    var Interfaceid = document.getElementsByName("Interfaceid");
    var blackName = document.getElementsByName("black");
    var mycars = [];
    for (var k = 0; k < blackName.length; k++) {

        if (blackName[k].checked == true) {
            mycars.push(Interfaceid[k].innerText)
        }
    }

    if (mycars.length > 1) {
        $.ajax({
            url: "/Deleteinterface",
            type: "POST",
            data: {"interface": mycars},
            cache: false,
            success: function (data) {
                if (data['code'] == 0) {
                    location.reload();
                } else {
                    alert(data['message'])
                }

            }
        })

    } else {
        alert("请选择接口")
    }

}


function check_form(type) {

    var Interfacename = $.trim($('#Interfacename').val());
    if (!Interfacename) {
        alert('用户ID不能为空！');
        return false;
    }
    var Interfacjson = $.trim($('#Interfacjson').val());
    var cc = Interfacjson.replace(/'/g, "\"");
    try {

        if (typeof JSON.parse(cc) == "object") {
            var d = $('#AddInterface').serializeArray();
            var form_data = {};
            $.each(d, function () {
                form_data[this.name] = this.value;
            });

            if (type == 'Add') {
                $.ajax(
                    {
                        url: "/AddInterface",
                        data: {"AddInterface": JSON.stringify(form_data)},
                        type: "post",
                        dataType: "json",
                        success: function (data) {
                            if (data['code'] == 0) {
                                location.reload();
                            } else {
                                alert(data['message'])
                            }
                        }
                    });
            } else if (type == 'Save') {
                $.ajax(
                    {
                        url: "/Saveinterface",
                        data: {"Saveinterface": JSON.stringify(form_data)},
                        type: "post",
                        dataType: "json",
                        success: function (data) {
                            if (data['code'] == 0) {
                                location.reload();
                            } else {
                                alert(data['message'])
                            }
                        }
                    });
            }
            $("#addInterface").modal("hide");
        } else {
            alert('请输入正确json！');
        }
    } catch (e) {
        alert('请输入正确json！');
    }


}

function Interfacedetails(str) {
    $("#baocun").css('display', 'inline');
    $("#tijiao").css('display', 'none');
    $.ajax({
        url: "/Interfacedetails",
        type: "POST",
        data: {"Interfacedetails": $(str).text()},
        cache: false,
        dataType: "json",
        success: function (data) {
            try {
                var json = eval("(" + data + ")");
                $("#Interfaceid").val(json[0]);
                $("#Interfacename").val(json[1]);
                $("#Interfacjson").val(json[2]);
            } catch (e) {
                alert(data['message'])
            }
        }
    });


    $("#addInterface").modal("show");
}


setTimeout(function () {
    document.getElementById("myAlert").style.display = "none";
}, 3000);