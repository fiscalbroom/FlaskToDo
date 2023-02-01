class Service {
    constructor() {
        this._baseUrl = 'api/todos';
        this.getAll = this.getAll.bind(this);
        this.add = this.add.bind(this);
        this.update = this.update.bind(this);
        this.delete = this.delete.bind(this);
    }

    _isJsonResponse(contentType) {
        return ((contentType || '').indexOf('application/json') > -1);
    }

    _getJsonReqHeaders(json) {
        return new Headers({
            'content-type': 'application/json',
            'content-length': json.length
        });
    }

// Async keword guarantees that the function will return a promise / thenable
    async _makeRequest(url, option) {
        const response = await fetch(url, option),
            { status, headers } = response,
            isJson = this._isJsonResponse(headers.get('content-type')),
            data = isJson ? await response.json() : await response.text();

        if (status >199 && status < 300) {
            return data;
        }

        const defaultMsg = 'Richiesta fallita a causa di un errore del server';
        const message = (isJson) ? (data.message || defaultMsg) : data || defaultMsg;

        throw new Error(message);

    }

    getAll() {
        return this._makeRequest(this._baseUrl);
    }

    add(text) {
        const body = JSON.stringify(todo),
            headers = this._getJsonReqHeaders(body);

        return this._makeRequest( '${this._baseUrl}/${todo.id}', {
            method: 'PUT',
            headers,
            body
        });
    }

    delete(id) {
        return this._makeRequest('${this._baseUrl}/${id}', {
            method: 'DELETE'
        });
    }
}

export const ToDoService = new Service();