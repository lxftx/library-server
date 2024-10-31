/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./src/js/modules/modal.js":
/*!*********************************!*\
  !*** ./src/js/modules/modal.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
function modal() {
    const body = document.querySelector('body'), 
        modal = document.querySelector('.modal'),
        navigateAuth = document.querySelector('.navigate__auth'),
        formAdd = document.querySelector('.form__add'),
        domen = window.location.origin,
        // domen = "http://localhost:8000/",
        djModel = window.location.pathname.split('/')[window.location.pathname.split('/').length - 1];
        // djModel = "languages";

    let acc, text_error, sh_alert = 0;

    IsLogin();
    closeModal();

    getData();

    addEventCreateRecord(formAdd);

    navigateAuth.addEventListener('click', (e) => {
        if (!IsLogin()) {
            openModal();
            createAuthForm();
            addEventAuthForm(modal);
        } else {
            Logout()
        }
    });

    function clickBtnCancel() {
        modal.querySelector('.modal__btn-cancel').addEventListener('click', () => {
            closeModal();
        });
    }

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            e.preventDefault();
        };
        if (e.key === 'Escape') {
            closeModal();
        };
    });

    function openModal() {
        modal.style.display = 'block';
        body.style.overflow = 'hidden';
    }

    function closeModal() {
        modal.style.display = '';
        body.style.overflow = '';
        clearModal();
    }

    function formReset() {
        modal.querySelector('.modal__form-error').remove()
        modal.querySelectorAll('input').forEach(item => item.style.borderColor = 'black');
    }

    function clearModal() {
        modal.querySelectorAll('.modal__form').forEach(item => item.remove());
    }

    function buttonEndDis(event) {
        const btn = modal.querySelector('button');
        if (event) {
            btn.disabled = true;
            btn.style.backgroundColor = '#cdcdcd';
        } else {
            btn.disabled = false;
            btn.style.backgroundColor = 'black';
        }
    }

    function IsLogin() {
        if (localStorage.getItem('acc') && localStorage.getItem('dt')) {
            const dateNow = new Date(),
                localDate = new Date(localStorage.getItem('dt'));
            if (localDate > dateNow) {
                document.querySelector('.navigate__auth').querySelector('img').src = "/static/icons/user-block-alt-svgrepo-com.svg";
                acc = localStorage.getItem('acc');
                return true;
            };
        };
        return false;
    }

    // Получаем CSRF-токен из куки
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Проверяем, соответствует ли кука искомому имени
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    async function authAccount(form) {
        const formData = new FormData(form),
            data = Object.fromEntries(formData.entries());

        let authStatus = true;
        buttonEndDis(true);
        if (modal.querySelector('.modal__form-error')) formReset();

        await fetch(domen + "/users/login/", {
            method: "POST",
            headers: {
                    "Content-type": "application/json",
                    "X-CSRFToken": getCookie('csrftoken')
            },
            credentials: 'include',
            body: JSON.stringify(data)
        })
        .then(data => data.ok ? data.json() : Promise.reject(data))
        .then(data => setAccountParameter(data))
        .then(data => Authenticate(data))
        .catch(data => {
            authStatus = errorHandler(data.status);
            setTimeout(addHtmlTextError, 2000);
        });

        if (authStatus) {
            closeModal();
            form.reset();
        };
    }

    function Authenticate(json_data) {
        if (!IsLogin()) {
            acc = json_data.acc;
            navigateAuth.querySelector('img').src = "/static/icons/user-block-alt-svgrepo-com.svg";
        };
        return true;
    }

    function Logout() {
        acc = undefined;
        if (localStorage.getItem('dt')) localStorage.removeItem('dt');
        if (localStorage.getItem('acc')) localStorage.removeItem('acc');
        navigateAuth.querySelector('img').src = "/static/icons/user-svgrepo-com.svg";
    }

    async function getRefreshToken() {
        let refreshStatus = true;``
        await fetch(domen + '/users/refresh/', {
            method: "POST",
            headers: {
                'Content-type': 'application/json',
                "X-CSRFToken": getCookie('csrftoken')
            },
            credentials: 'include'
        })
        .then(data => data.ok ? data.json() : Promise.reject(data))
        .then(data => setAccountParameter(data))
        .then(data => Authenticate(data))
        .catch(data => {
            refreshStatus = errorHandler(data.status);
            ShowAlert(text_error, "#f71818c9");
        });
        return refreshStatus;
    }

    function IsAuth() {
        if (!acc) {
            ShowAlert("Вы не авторизованны!", "#ffbd43c9");
            return false;
        };
        return true;
    }

    function setAccountParameter(json_data) {
        let dateNow = new Date(),
            dateMillis = dateNow.getTime(),
            timePeriod = "00:05:00",
            parts = timePeriod.split(/:/),
            timePeriodMillis = (parseInt(parts[0], 10) * 60 * 60 * 1000) +
                                (parseInt(parts[1], 10) * 60 * 1000) +
                                (parseInt(parts[2], 10) * 1000),
            newDate = new Date();
            newDate.setTime(dateMillis + timePeriodMillis);

        if (localStorage.getItem('acc') && localStorage.getItem('dt')) {
            if (new Date(localStorage.getItem('dt')) < dateNow) {
                localStorage.setItem('dt', newDate);
                localStorage.setItem('acc' , json_data.acc);
            };
        } else {
            localStorage.setItem('dt', newDate);
            localStorage.setItem('acc' , json_data.acc);
        };
    }


    function createAuthForm() {
        const htmlFormAuth = `
        <div class="modal__form">
            <img class="modal__btn-cancel" src="/static/icons/cross-svgrepo-com.svg">
            <form action="" method="post" class="form__auth">
                <div class="modal__form-info">
                    <input class="modal__form-input" name="username" type="text" id="#username" placeholder="Имя пользователя">
                    <input class="modal__form-input" name="password" type="password" id="#password" placeholder="Ваш пароль">
                </div>
                <button class="modal__form-btn" type="submit">Войти!</button>
            </form>
        </div>`;
        modal.innerHTML += htmlFormAuth;
    }
    

    function addEventAuthForm() {
        clickBtnCancel();
        const formAuth = modal.querySelector('form');
        formAuth.addEventListener('submit', (e) => {
            e.preventDefault();
            authAccount(formAuth);
        });
    }

    function errorHandler(status) {
        if (status == 400) {
            text_error = "Ошибка сервера! :(";
        } else if (status == 401) {
            text_error = 'Имя пользователя и пароль не найдены в системе! :(';
        } else {
            text_error = 'Ошибка сервера! :(';
        };
        return false;
    }

    function addHtmlTextError() {
        const htmlText = 
        `
        <div class="modal__form-error">${text_error}</div>
        `, modalForm = modal.querySelector('.modal__form');
        if (!modalForm.querySelector('.modal__form-error')) {
            modalForm.innerHTML += htmlText;
            modalForm.querySelectorAll('input').forEach(item => item.style.borderColor = 'red');
        };
        addEventAuthForm(modal);
        buttonEndDis(false);
    }


    function ShowAlert(message, color) {
        if (sh_alert)  return true; 
        const alertWindow = document.createElement('div'),
            alertImg = document.createElement('img'),
            alertText = document.createElement('div');
        
        alertWindow.classList.add('alert');
        alertImg.classList.add('alert-img');
        alertText.classList.add('alert__text');
        
        alertText.textContent = message;
        alertImg.src = "/static/icons/cross-svgrepo-com.svg";
        alertWindow.style.backgroundColor = color;

        alertWindow.append(alertImg, alertText)
        body.prepend(alertWindow);
        let timeOut = setTimeout(() => {HideAlert(alertWindow); sh_alert = 0}, 3000);

        alertImg.addEventListener('click', () => {
            HideAlert(alertWindow);
            clearTimeout(timeOut);
        })
        sh_alert = 1;
    }

    function HideAlert(alertSelector) {
        alertSelector.remove();
    }

    function triggerFormSubmit(form, event_param) {
        // Создаем новое событие submit
        const event = new Event(`${event_param}`, {
            bubbles: true,  // Событие будет всплывать
            cancelable: true  // Событие можно отменить
        });
    
        // Запускаем событие на форме
        form.dispatchEvent(event);
    }

    function addEventCreateRecord(form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            createRecord(form)
        });
    }

    async function createRecord(form) {
        let createStatus = true;
        if (!IsAuth()) return false
        const formData = new FormData(form),
            data = Object.fromEntries(formData.entries());

        await fetch(domen + `/api/v1/${djModel}/`, {
            method: "POST",
            headers: {
                "Content-type": "application/json",
                "Authorization": `Bearer ${acc}`,
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include',
            body: JSON.stringify(data)
        })
        .then(data => data.ok ? data.json() : Promise.reject(data))
        .then(() => { 
            getData(); 
            ShowAlert('Успешное сохранение!', '#3bf33bd4');
        })
        .catch(async data => {
            createStatus = false
            if (data.status == 401) {
               if (await getRefreshToken()) {
                    // Ручной запуск submit
                    triggerFormSubmit(formAdd, 'submit');
                };
            } else {
                errorHandler(data.status);
                ShowAlert(text_error, '#f71818c9');
            }; 
        });

        if (createStatus) {
            form.reset();
        };
    }

    function getData() {
        fetch(domen + `/api/v1/${djModel}/`, {
            method: "GET",
            headers: {
                "Content-type": "Application/json"
            },
            credentials: 'include'
        })
        .then(data => data.ok ? data.json() : Promise.reject(data))
        .then(data => updateTable(data))
        .catch(data => {
            errorHandler(data.status);
            ShowAlert(text_error, "#f71818c9");
        });
    };

    function clearTable() {
        const tbody = document.querySelector('tbody'),
            trs = tbody.querySelectorAll('tr');
        trs.forEach((item, index) => {
            if (index != 0) item.remove();
        });
        return tbody;
    }

    function updateTable(json_data) {
        const tbody = clearTable();
        json_data.forEach((item, index) => {
            const htmlRecords = `
            <tr>
                <td>${index + 1}</td>
                <td>${item.name ? item.name : item.last_name + " " + item.first_name}</td>
                <td class="form">
                    <button class="form__event-open" value="${item.id}">
                        <img src="/static/icons/check-tick-svgrepo-com.svg">
                    </button>
                    <button class="form__event-delete" value="${item.id}">
                        <img src="/static/icons/cancel-20px-svgrepo-com.svg">
                    </button>
                </td>
            </tr>
            `
            tbody.innerHTML += htmlRecords;
            addEventUpdateRecord();
            addEventDeleteRecord();
        })
    }

    async function deleteRecord(item, id) {
        if (!IsAuth()) return false
        await fetch(domen +`/api/v1/${djModel}/${id}/`, {
            method: "DELETE",
            headers: {
                "Content-type": "application/json",
                "Authorization": `Bearer ${acc}`,
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include'
        })
        .then(data => data.status == 200 ? data.json() : Promise.reject(data))
        .then(() => getData())
        .then(() => ShowAlert('Успешное удаление!', '#3bf33bd4'))
        .catch(async data => {
            if (data.status == 401) {
                if (await getRefreshToken()) {
                    // Ручной запуск click
                    triggerFormSubmit(item, 'click');
                };
            } else {
                errorHandler(data.status);
                ShowAlert(text_error, '#f71818c9');
            };
        });
    }

    function addEventDeleteRecord() {
        const btnDelete = document.querySelectorAll('.form__event-delete');
        if (btnDelete.length == 0) return false;
        btnDelete.forEach(item => {
            item.addEventListener('click', (e) => {
                deleteRecord(item, item.value);
            }) 
        }) 
    }

    async function getRecordForId(item, id) {
        await fetch(domen + `/api/v1/${djModel}/${id}/`, {
            method: 'GET',
            headers: {
                'Content-type': 'application/json',
                "Authorization": `Bearer ${acc}`
            },
            credentials: 'include'
        })
        .then(data => data.ok ? data.json() : Promise.reject(data))
        .then(data => createUpdateRecordForm(data))
        .then(data => updateRecord(data))
        .catch(async (data) => {
            if (data.status == 401) {
                if (await getRefreshToken()) {
                    // Ручной запуск click
                    triggerFormSubmit(item, 'click');
                };
            } else {
                errorHandler(data.status);
                ShowAlert(text_error, '#f71818c9');
            };
        });
    }

    function updateRecord(dt) {
        const formUpdate = document.querySelector(".form__update");
        formUpdate.addEventListener("submit", (e) => {
            e.preventDefault();
            let updateStatus = true;
            const formData = new FormData(formUpdate),
                data = Object.fromEntries(formData.entries());

            fetch(domen + `/api/v1/${djModel}/${dt.id}/`, {
                method: "PUT",
                headers: {
                    "Content-type": "application/json",
                    'X-CSRFToken': getCookie('csrftoken'),
                    "Authorization": `Bearer ${acc}`
                },
                credentials: "include",
                body: JSON.stringify(data)
            })
            .then(data => data.ok ? getData() : Promise.reject(data))
            .catch( async (data) => {
                if (data.status == 401) {
                    if (await getRefreshToken()) {
                        // Ручной запуск click
                        triggerFormSubmit(formUpdate, 'sumbit');
                    };
                } else {
                    errorHandler(data.status);
                    ShowAlert(text_error, '#f71818c9');
                };
            })

            if (updateStatus) {
                closeModal();
                ShowAlert("Удачное сохранение!", '#3bf33bd4');
            };
        });
    }

    function createUpdateRecordForm(data) {
        const formInfo = document.querySelector('.form__add').querySelectorAll('.form__input');
        let inputForm = '';
        formInfo.forEach(item => {
            const tag = item.cloneNode(true);
            inputForm += tag.outerHTML.trim();
        });
        const htmlFormUpdate =
        ` 
        <div class="modal__form">
            <img class="modal__btn-cancel" src="/static/icons/cross-svgrepo-com.svg">
            <form action="" method="post" class="form__update">
                <div class="modal__form-info">
                    ${inputForm}
                </div>
                <button class="modal__form-btn" type="submit">Сохранить!</button>
            </form>
        </div>`;
        modal.innerHTML += htmlFormUpdate;
        
        openModal();
        clickBtnCancel();

        modal.querySelectorAll('.form__input').forEach(item => {
            item.classList = "modal__form-input";
            if (item.tagName == "SELECT") {
                for (let option of item.querySelectorAll("option")) {
                    if (typeof(data[item.name]) == "object") {
                        for (let name of data[item.name]) {
                            if (option.textContent == name) {
                                option.selected = true;
                            };
                            if (typeof(name) == "object" && option.value == name.id) {
                                option.selected = true;
                            }
                        };
                    } else  {
                        if (option.textContent == data[item.name]) {
                            console.log(option);
                            option.selected = true;
                        };
                    };
                };
            } else {
                item.value = data[item.name];
            };
            // item.value = data[item.name];
        });

    }

    function addEventUpdateRecord() {
        const btnUpdate = document.querySelectorAll('.form__event-open');
        if (btnUpdate.length == 0) return false;
        btnUpdate.forEach(item => {
            item.addEventListener('click', () => {
                if (!IsAuth()) return false
                getRecordForId(item, item.value);
            });
        });
    }
}

/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (modal);

/***/ }),

/***/ "./src/js/modules/slider_form.js":
/*!***************************************!*\
  !*** ./src/js/modules/slider_form.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
function slider_form() {
    const contentBlocks = document.querySelectorAll('.content__block'),
        inner = document.querySelector('.content__block-inner'),
        prevButton = document.querySelector('.prev'),
        nextButton = document.querySelector('.next'),
        listTd = document.querySelectorAll('td'),
        form = document.querySelector('form');
    let indexBlock = 1;
    inner.style.width = contentBlocks.length * 100 + '%';
    const width = window.getComputedStyle(inner).width.match(/\d+/g)[0] / 2;
    
    listTd.forEach(item => {
        if (item.textContent.search("None") != -1) {
            item.textContent = item.textContent.replace("None", "").trim();
        };
    });

    flipBlocks(0);

    prevButton.addEventListener('click', () => {
        flipBlocks(indexBlock += -1);
    });

    nextButton.addEventListener('click', () => {
        flipBlocks(indexBlock += 1);
    });

    function flipBlocks () {
        if (indexBlock > contentBlocks.length) indexBlock = 1;
        if (indexBlock < 1) indexBlock = contentBlocks.length;

        const offer = width * (indexBlock - 1);
        inner.style.transform = `translateX(-${offer}px)`; 
        
        contentBlocks.forEach(item => {
            if (item == contentBlocks[indexBlock - 1]) {
                item.style.height = '';
            } else {
                item.style.height = '0';
            }; 
        });
    }

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        console.log(document.URL);
    });
}

/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (slider_form);

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};
// This entry need to be wrapped in an IIFE because it need to be isolated against other modules in the chunk.
(() => {
/*!***************************!*\
  !*** ./src/js/scripts.js ***!
  \***************************/
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _modules_modal__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./modules/modal */ "./src/js/modules/modal.js");
/* harmony import */ var _modules_slider_form__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./modules/slider_form */ "./src/js/modules/slider_form.js");



document.addEventListener('DOMContentLoaded', () => {
    (0,_modules_slider_form__WEBPACK_IMPORTED_MODULE_1__["default"])();
    (0,_modules_modal__WEBPACK_IMPORTED_MODULE_0__["default"])();
});
})();

/******/ })()
;
//# sourceMappingURL=bundle.js.map