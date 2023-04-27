window.addEventListener('DOMContentLoaded', function (){
    //весь код который мы напишем в этой функции будет исполен когда dom дерево будет загужено в браузере  let form = document.getElementById('form');
    form.addEventListener('submit', checkTest);

    function checkTest(event) {

        event.preventDefault();

        let fields = document.querySelectorAll('.exercises_field');

        for (let i = 0; i < fields.length; ++i) {

            let v = fields[i].value
            let answer = fields[i].getAttribute('data_answer')
         
  
            if (v.toLowerCase() === answer) {
                if (fields[i].classList.contains("error")) {
                    fields[i].classList.remove('error');
                }
                fields[i].classList.add('correct');
            }

            else {
                if (fields[i].classList.contains("correct")) {
                    fields[i].classList.remove('correct');
                }
                fields[i].classList.add('error');
            }
        }

    }
})

