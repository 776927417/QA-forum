//alert("register.js") // 测试是否弹出小框
// 整个网页加载完毕才会执行$function部分
// 发送验证码步骤：
// 1. 获取输入的邮箱地址，
// 2. 点击按钮生成并发送验证码，
// 3. 验证用户输入的验证码和发送是否一致
function bindEmailCaptchaClick(){
    $("#captcha-btn").click(function(event){ // 通过“#”号获取html中的id(captcha-btn)
        var $this = $(this) //'$this' 是当前按钮的jquery对象
        event.preventDefault(); // 按钮有时默认提交web，这里阻止默认

    //通过[name='']获取html中的name
    var email = $("input[name='email']").val(); // val()获取输入框的值
    // alert(email); //弹窗测试一下，是否收到验证码
    $.ajax({
        url:"/auth/captcha/email?email="+email, //发送用户填写的email到后端
        // 如果没有指定method，默认get请求
        method:"GET",
        success:function(result){
            var code = result['code'];
            if(code == 200){
                var countdown = 5;
                $this.off("click")                           //准备开始倒计时，让'获取验证码'button变得不可点击
                var timer = setInterval(function(){ // 倒计时ing
                    $this.text(countdown);                                // 每一秒显示一次时间
                    countdown -= 1;
                    if(countdown <= 0){                 // 倒计时不能为负数
                        clearInterval(timer);           // 清除定时器
                        $this.text("获取验证码")           // 重新上线'获取验证码'button
                        bindEmailCaptchaClick();        // call自己，可以重复以上动作
                    }
                },1000)
                alert("verify code sent")
            }else{
                alert("not success")
            }
        },
        fail:function(error){
            console.log(error);
        }
    })
    })
}

$(function (){
    bindEmailCaptchaClick();
})
