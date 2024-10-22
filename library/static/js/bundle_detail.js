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
    const modal = document.querySelector('.modal'),
    btnOpen = document.querySelectorAll('.form__event-open'),
    body = document.querySelector('body'),
    btnCancel = document.querySelector('.modal__btn-cancel'),
    modalForm = document.querySelector('.modal__form'),
    formSave = modalForm.querySelector('.form__save'),
    auth = document.querySelector('.navigate__auth');

    formSave.remove();

    auth.addEventListener('click', () => {
        const formAuth = document.createElement('form'),
            formInfo = document.createElement('div'),
            username = document.createElement('input'),
            password = document.createElement('input'),
            btn = document.createElement('button');

        formAuth.method = 'POST';  formAuth.classList = "form__auth";
        formInfo.classList.add('modal__form-info');
        username.id = 'username'; username.name = 'username'; username.type = 'text'; username.placeholder = "Имя пользователя"; username.classList.add('modal__form-input');
        password.id = 'password'; password.name = 'password'; password.type = 'password'; password.classList.add('modal__form-input'), password.placeholder = 'Ваш пароль';
        btn.classList = 'modal__form-btn'; btn.type = 'submit'; btn.textContent = "Войти!";
        
        formInfo.append(username, password);
        formAuth.append(formInfo, btn);
        modalForm.append(formAuth);

        addShowModal();
    });

    btnOpen.forEach(item => {
        item.addEventListener('click', () => {
            modalForm.append(formSave);
            addShowModal();
        })
    });

    btnCancel.addEventListener('click', () => {
        deleteShowModal();
    })

    document.addEventListener('keydown', (event) => {
        if (window.getComputedStyle(modal).display == 'block' && event.key == 'Escape') deleteShowModal();
        if (event.key == 'Tab') event.preventDefault();
    });

    function addShowModal() {
        modal.style.display = 'block';
        body.style.overflow='hidden';
    }

    function deleteShowModal() {
        if (modalForm.lastChild == formSave) {
            formSave.remove();
        } else {
            modalForm.querySelector('.form__auth').remove();
        };
        modal.style.display = 'none';
        body.style.overflow='';
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