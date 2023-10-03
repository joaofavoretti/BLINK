import api from './api'

export default class StatisticsService {
    static async getAmountValidated() {
        return await api.get('/statistics/amount_validated')
    }

    static async getAmountOnline() {
        return await api.get('/statistics/amount_online')
    }

    static async getConfidence() {
        return await api.get('/statistics/confidence')
    }

    static async save() {
        return await api.post('/statistics/save')
    }
}