var width = {{ad_params.width}};
var height = {{ad_params.height}};
{% if ad_params.tweenmax=='on' %}
    {% if ad_params.sample_animation=='on' %}
        // basic animation
        TweenMax.fromTo('#text', 0.2, {opacity:0, y:-10}, {delay:0.2, opacity:1, y:0});
        TweenMax.fromTo('#product', 0.4, {x:50}, {delay:0.4, opacity:1, x:0});
        TweenMax.to('#text', 0.2, {delay:2, opacity:0, y:10});
        TweenMax.to('#product', 0.2, {delay:2.0, opacity:0, x:-50});
        TweenMax.fromTo('#logo', 0.6, {opacity:0, y:height/2-22}, {delay:2.4, opacity:1, y:height/2-12});
    {% endif %}
{% endif %}


