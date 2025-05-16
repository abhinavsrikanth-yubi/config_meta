// config.js - Only add new Q/A pairs, no remove button logic

document.addEventListener('DOMContentLoaded', function () {
    var addBtn = document.querySelector('.add-qa');
    if (addBtn) {
        addBtn.addEventListener('click', function(e) {
            e.preventDefault();
            let container = document.getElementById('qa-container');
            let totalForms = document.querySelector('[name="parent_response-TOTAL_FORMS"]');
            let formIdx = parseInt(totalForms.value);
            let emptyFormHtml = document.getElementById('empty-form').innerHTML.replace(/__prefix__/g, formIdx);
            container.insertAdjacentHTML('beforeend', emptyFormHtml);
            totalForms.value = formIdx + 1;
        });
    }
});

            e.preventDefault();
            let pair = e.target.closest('.qa-pair');
            if (document.querySelectorAll('.qa-pair').length > 1) {
                pair.remove();
                updateDropdowns();
            }

    // Update dropdowns on change
    document.getElementById('qa-container').addEventListener('change', function (e) {
        if (e.target.classList.contains('question-dropdown')) {
            updateDropdowns();
        }
    });

    // Initial update
    updateDropdowns();