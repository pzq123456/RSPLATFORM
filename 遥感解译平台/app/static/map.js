var map = new BMapGL.Map("container");

var point = new BMapGL.Point(120.131267, 36.005814);//学校南门
map.centerAndZoom(point, 15);// 创建地图实例 

var width=700;
var height=500;

var displayData= function(data){

            for (let i = 0; i < data.length; i++) 
            {
                let vpoint = new BMapGL.Point(data[i].lon,data[i].lat);//创建点
                let title=data[i].user+"的帖子";
                //在此处动态生成html模板插入content中
                let avatar_path="https://gravatar.loli.net/avatar/"+data[i].digest+"?d=identicon&s=16";

                let post_content=['<center>',
                '   <form action = "/comment" method = "post">',
                '      <label for = "post_id">帖子编号</label><br>',
                '      <input type = "int" name = "post_id"/><br>',
                '      <label for = "content">跟帖内容</label><br>',
                '      <textarea name = "content" style="width: 200px;height:100px;"></textarea><br>',
                '      <input type = "submit" value = "Submit" />',
                '   </form>',
                ].join("");
                post_content=post_content+
                ['<table border="1">',
                '<tbody>',
                '    <tr>',
                '        <td><img src='+avatar_path+'></td>',
                '        <td>'+'楼主'+data[i].user+'<br>'+data[i].content+
                '        </td>',
                '    </tr>   ',
                '</tbody>',
            '</table>','</center>'].join("");
                add_simple_infowindow_on_map(map,vpoint,width,height,title,post_content,data[i].digest,data[i].post_id);                            
            } 
        }


        $.ajax({
            url: "/JSON",
            type: "GET",
            dataType: "json",
            success: 
            function (data) {
                displayData(data)
            }
        });





var html_content=['<center>',
'   <form action = "/map" method = "post">',
'      <label for = "lon">经度</label><br>',
'      <input type = "float" name = "lon" placeholder ="120.131267"/><br>',
'      <label for = "lat">纬度</label><br>',
'      <input type = "float" name = "lat" placeholder ="36.005814"/><br>',
'      <label for = "content">留言内容</label><br>',
'      <textarea name = "content" placeholder = "Hello World!" style="width: 500px;"></textarea><br>',
'      <input type = "submit" value = "Submit" />',
'   </form>',
'</center>'].join("");

//html_content=html_content+"<br><hr/>{%- for message in get_flashed_messages() %}{{ message }}{%- endfor %}"


map.addEventListener('click', function (e) {
    alert('点击位置经纬度：' +'经度：'+ e.latlng.lng + '纬度：'+ e.latlng.lat+ " 请将鼠标移至点上进行留言");
    var new_point=new BMapGL.Point(e.latlng.lng, e.latlng.lat);
    add_html_infowindow_on_map(map,new_point,width,height,"<center><h7 style='color:#4798cf;'>地图留言板：</h7></center>",html_content);
});


//封装进函数 创建简单信息窗口（不含HTML）
function add_simple_infowindow_on_map(map,my_point,win_width,win_height,title_text,content_text,authorname,post_id) {
	
    var myIcon = new BMapGL.Icon("https://gravatar.loli.net/avatar/"+authorname+"?d=identicon&s=32", new BMapGL.Size(32, 32)); //添加用户头像
    var marker = new BMapGL.Marker(my_point,{ icon: myIcon });  // 创建标注
    map.addOverlay(marker);              // 将标注添加到地图中
	var opts = {
	    width : win_width,     // 信息窗口宽度
	    height: win_height,     // 信息窗口高度
	    title : title_text , // 信息窗口标题
	   
	}

var infoWindow = new BMapGL.InfoWindow(content_text, opts);  // 创建信息窗口对象 
marker.addEventListener('mouseover', function(){     
        map.openInfoWindow(infoWindow, my_point); //开启信息窗口
        //现在需要获取该信息窗口对应的帖子编号 并利用ajax向后端请求跟帖内容    
        var active_info_win_content=document.querySelector('.BMap_bubble_content');//获取当前打开的信息窗口
        var form= active_info_win_content.querySelector("form"); 
        var fpost_id=form.childNodes[4];
        fpost_id.value=post_id;
        //alert(post_id);//测试完成 正常显示帖子的编号
        //此处可以加js代码来操控信息窗口的内容！
        //var active_info_bubble=document.querySelector('.BMap_bubble_pop');//获取当前打开的信息窗口
        //先请求该点的评论表
        $.ajax({
            url: "/FOLLOWPOST/"+ post_id,      
            type: "GET",
            dataType: "json",
            success: 
            function (data) {
                make_table_by_Data(data)
            }
        });
        
        var make_table_by_Data= function(data){
            for (let i = 0; i < data.length; i++) {

                let post_table=active_info_win_content.querySelector('tbody');//获取信息窗口内表格（楼主表） 
                let avatar_path="https://gravatar.loli.net/avatar/"+data[i].digest+"?d=identicon&s=16";
                let tr = document.createElement('tr');
                post_table.appendChild(tr); //创建行
                    let td_ava = document.createElement('td');
                    td_ava.innerHTML = "<img src="+avatar_path+"></img>"+"<br>"+data[i].user;
                    tr.appendChild(td_ava); //创建列
                    let td_cont = document.createElement('td');
                    td_cont.innerText = data[i].content;
                    tr.appendChild(td_cont); //创建列
            }

        }





        









        /*
        var but_in_win=active_info_win_content.querySelectorAll("button");
        but_in_win[0].addEventListener("click",but_1_fun);//添加事件处理程序
        function but_1_fun(){alert("按钮1的事件处理程序!");}
        but_in_win[1].addEventListener("click",vut_2_fun);//添加事件处理程序
        function vut_2_fun(){alert("按钮2的事件处理程序!");}
        infoWindow.addEventListener("close",function(){alert("信息窗口已关闭!");infoWindow.removeEventListener('close');but_in_win[0].removeEventListener("click",but_1_fun);but_in_win[1].removeEventListener("click",vut_2_fun);})
        */
	})
     
}



map.enableScrollWheelZoom(true);   //开启鼠标滚轮缩放



function add_html_infowindow_on_map(map,my_point,win_width,win_height,title_text,content_text) {
var marker = new BMapGL.Marker(my_point);  // 创建标注
map.addOverlay(marker);              // 将标注添加到地图中
var opts = {
    width : win_width,     // 信息窗口宽度
    height: win_height,     // 信息窗口高度
    title : title_text , // 信息窗口标题  
}

var infoWindow = new BMapGL.InfoWindow(content_text, opts);  // 创建信息窗口对象 
marker.addEventListener('mouseover', function(){          
    map.openInfoWindow(infoWindow, my_point); //开启信息窗口
    //此处可以加js代码来操控信息窗口的内容！
    var active_info_bubble=document.querySelector('.BMap_bubble_pop');//获取当前打开的信息窗口
    var active_info_win_content=document.querySelector('.BMap_bubble_content');//获取当前打开的信息窗口
    var form= active_info_win_content.querySelector('form');

    //获取当前打开的信息窗口 并将位置信息预先填入其中
    var lon=form.childNodes[4];
    lon.value=my_point.lng;
    var lat=form.childNodes[10];
    lat.textContent=my_point.lat;
    lat.value=my_point.lat;

}); 
 
}



