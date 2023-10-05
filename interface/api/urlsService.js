import api from './api'

export default class UrlsService {
    static baseURI = '/urls'

    static async getList() {
        const url = `${UrlsService.baseURI}/`
        return await api.get(url)
    }

    static async getAvailableCommoncrawlFiles(amount=5) {
        const url = `${UrlsService.baseURI}/available_commoncrawl_files`
        const params = { amount }
        return await api.get(url, { params })
    }
}