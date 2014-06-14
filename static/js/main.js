$(document).ready(function () {
    $(".panel-body, p, pre, strong, em").each(function() {
    var text = $(this).html();
    pattern = /[^>]#[A-Za-z0-9]+/g
    tag = ""

    while(tag = pattern.exec(text)){
        console.log(tag.toString(),tag.toString().substring(1))
        replacement="<a class='hashtag' href='/?query="+tag.toString().substring(2)+"'>"+tag.toString().substring(1)+"</a> "
        text = text.replace(tag.toString(),replacement);
    }
    $(this).html(text);
});
});
