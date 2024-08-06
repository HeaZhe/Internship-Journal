import axios from "axios"
import { ACCESS_TOKEN } from "./constants" 

const apiUrl = "https://0e316787-d53f-4448-b063-6a993f276814-dev.e1-us-east-azure.choreoapis.dev/djangoreacttutorial/backend/v1";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL : apiUrl,
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem(ACCESS_TOKEN)
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

export default api