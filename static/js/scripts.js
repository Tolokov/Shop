//4. Отправляем запрос
function ajaxSend(url, params) {
    fetch(`${url}?${params}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
        .then(response => response.json())
        .then(json => render(json))
        .catch(error => console.error(error))
}


//1. Поиск формы по запросу filter
const forms = document.querySelector('form[name=filter]');


//2. Когда у формы будет вызван метод submit, должна перезагрузиться страница, мы блокируем это действие
forms.addEventListener('submit', function (e) {
    e.preventDefault();
    //3. Получаем данные из формы
    let url = this.action;
    let params = new URLSearchParams(new FormData(this)).toString();
    ajaxSend(url, params);
});


//4. Рендер шаблона
function render(data) {
    let template = Hogan.compile(html);
    let output = template.render(data);

    const div = document.querySelector('.ajax>.row2');
    div.innerHTML = output;
}


//5. Блок в котором рендерится одна колонка
let html = '\
{{#json_answer}}\
<div class="col-sm-4">\
    <div class="product-image-wrapper">\
        <div class="single-products">\
            <div class="productinfo text-center">\
                <a href="../products/{{ pk }}" target="_blank">\
                    <img src="../../media/{{ fields.image }}" alt="{{ fields.name }}"/></a>\
                    <h2>${{ fields.price }}</h2><p><a href="../products/{{ pk }}"> {{ fields.name }}</a></p>\
                <div style="margin-right: 20px;"></div></div>\
        <img src="../../static/images/home/{{ fields.condition }}.png" class="new" alt="status"/>\
</div></div>\
<div class="single-products">\
                <div class="productinfo text-center">\
                    <div class="choose">\
                        <ul class="nav nav-pills nav-justified" style="">\
                            <div class="justify-center btn " style="margin:auto; margin-right: 20px;">\
\
                            </div>\
                        </ul>\
                    </div>\
                </div>\
            </div>\
            </div></div>\
{{/json_answer}}'


