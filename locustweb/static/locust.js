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
        myjson[k + 1] = mycars;
    }

    input.value = JSON.stringify(myjson);
    myForm.appendChild(input);
    myForm.submit();
}


//checkbox 全选/取消全选

function swapCheck() {
    var isCheckAll = false;
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