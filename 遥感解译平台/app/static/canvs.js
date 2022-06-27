/**********************************************************************
 * GLOBAL VARIABLES
 *********************************************************************/
var canvas, context;
var img,//图片对象
    imgIsLoaded,//图片是否加载完成;
    imgX = 0,
    imgY = 0,
    imgScale = 1;
var ori_img;//全局变量存储原始图片方便重置




//alert("{{img_path|safe}}")
 
(function int() {
    canvas = document.getElementById('canvasExampleFilters'); //画布对象
    //首先获取画布对象
    context = canvas.getContext('2d');//画布显示二维图片
    //然后获取二维画布的上下文
    loadImg();
})();

function loadImg() {
  img = new Image();
  img.onload = function () {
      imgIsLoaded = true;
      ori_img=img;
      drawImage();
  }//图片加载完成后调用该函数

  img.src = 'static/userimg/img_0.png';

}


function drawImage() {
    context.clearRect(0, 0, canvas.width, canvas.height);//每一次重绘图片之前清除画布

    context.drawImage(
        //相对于图片本身的参数
          img, //规定要使用的图像、画布或视频

          0, 0, //开始剪切的 x 坐标位置

          img.width, img.height,  //被剪切图像的高度

        //相对于画布的参数
          imgX, imgY,//在画布上放置图像的 x 、y坐标位置

          img.width * imgScale, img.height * imgScale  //图片展示时的尺寸（高度、宽度）
      );}
      


/*事件注册*/
function canvasEventsInit() {
    //鼠标点下后的事件
    canvas.onmousedown = function (event) {

    var posl = windowToCanvas(event.clientX, event.clientY);//将用户鼠标点击的位置转化为canvas中位置

    clix=posl.x;
    cliy=posl.y;

    var d1=cliy-imgY;//用户鼠标位置相对于图片绘制角点的坐标差值 每一次重新点击才会改变此值
    var d2=clix-imgX;

      canvas.onmousemove = function (evt) {  //移动
          canvas.style.cursor = 'grab';//设置鼠标样式为十字箭头

          var pos = windowToCanvas(evt.clientX, evt.clientY);
          var x = (pos.x-d2);
          var y = (pos.y-d1);
          imgX  = x;
          imgY  = y;
          //每一次用户按住图片并移动都会触发canvas重绘
          drawImage();  //重新绘制图片
      };

      canvas.onmouseup = function () {
        //鼠标抬起则清空事件
          canvas.onmousemove = null;
          canvas.onmouseup = null;
          canvas.style.cursor = 'default';//十字丝设置为默认
      };

  };

  canvas.onmousewheel = canvas.onwheel = function (event) {    //滚轮放大缩小

      var pos = windowToCanvas (event.clientX, event.clientY);
      event.wheelDelta = event.wheelDelta ? event.wheelDelta : (event.deltalY * (-40));  //获取当前鼠标的滚动情况

      if (event.wheelDelta > 0) {
      
       
            imgScale=imgScale*2;
          imgX = imgX * 2 - pos.x;
          imgY = imgY * 2 - pos.y;
        
          
      } else {
          imgScale=imgScale/2;
          imgX = imgX * 0.5 + pos.x*0.5;
          imgY = imgY * 0.5 + pos.y*0.5;
      }
      drawImage();   //重新绘制图片
  };
}


/*坐标转换*/
function windowToCanvas(x,y) {
  var box = canvas.getBoundingClientRect();  //这个方法返回一个矩形对象，包含四个属性：left、top、right和bottom。分别表示元素各边与页面上边和左边的距离
  return {
      x: x - box.left - (box.width - canvas.width) / 2,
      y: y - box.top - (box.height - canvas.height) / 2
  };
}




but_FiltersEdge = document.getElementById('FiltersEdge'); //获取第一个按钮
but_FiltersEdge.onmousedown=FiltersEdge;

function FiltersEdge(){
    var imageExampleFilters = new MarvinImage(img.width*imgScale, img.height*imgScale);
    var imageExampleFiltersOut = new MarvinImage(img.width*imgScale, img.height*imgScale);
    imageExampleFilters.image=img;
    imageExampleFilters.imageData=context.getImageData(imgX ,imgY, img.width*imgScale, img.height*imgScale);

    Marvin.prewitt(imageExampleFilters, imageExampleFiltersOut);
    
      img=imagedata_to_image(imageExampleFiltersOut.imageData);
      drawImage();
      
      
    
    
    
 
  
}


but_ReSet = document.getElementById('ReSet'); //获取第2个按钮
but_ReSet.onmousedown=ReSet;

function ReSet(){
    img=ori_img;
    drawImage();
}











canvasEventsInit()



//辅助函数
function imagedata_to_image(imagedata) {
  var canvas = document.createElement('canvas');
  var ctx = canvas.getContext('2d');
  canvas.width = imagedata.width;
  canvas.height = imagedata.height;
  ctx.putImageData(imagedata, 0, 0);
  var image = new Image();
  image.src = canvas.toDataURL();
  return image;

}