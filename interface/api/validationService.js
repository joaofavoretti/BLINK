import api from './api'

export default class ValidationService {

    static async getList() {
        return await api.get('/validation/get_list')
    }

    static async getDocument(id) {
        return await api.get(`/validation/get_document/${id}`)
    }

    static async getNextDocument(id) {
        return await api.get(`/validation/get_next_document/${id}`)
    }

    static async updateDocument(id, data) {
        return await api.put(`/validation/update_document/${id}`, data)
    }
}