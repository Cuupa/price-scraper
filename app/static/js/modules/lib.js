export function html(tag, ...classList) {
    let element = document.createElement(tag);
    if(classList) {
        element.classList.add(...classList);
    }
    return element;
}

export function tr(id) {
    let tr = html('tr')
    if(id) {
        tr.setAttribute("id", id);
    }
    return tr;
}

export function th(content) {
    let th = html('th');
    if(content) {
        th.textContent = content;
    }
    return th;
}

export function td(content, ...classList) {
    let td = html('td', ...classList);
    if(content) {
        td.textContent = content;
    }
    return td;
}

export function a(href, text, ...classList) {
    let link = html('a', ...classList);
    link.setAttribute("href", href);
    link.textContent = text;
    return link;
}

export function button(text, id, ...classList) {
    let button = html('button', ...classList);
    if(text) {
        button.textContent = text;
    }
    if(id) {
        button.setAttribute('id', id);
    }
    return button;
}

export function input(value, id, type, disabled) {
    let input = html('input');
    if(value) {
        input.setAttribute('value', value);
    }
    if(id) {
        input.setAttribute('id', id);
    }
    if(type) {
        input.setAttribute('type', type);
    }
    if(disabled) {
        input.setAttribute('disabled', disabled);
    }

    return input;
}

