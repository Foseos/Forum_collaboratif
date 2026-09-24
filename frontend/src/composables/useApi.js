import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  // On ne fixe pas de Content-Type global ici, 
  // car axios le gère automatiquement selon le type de payload (ex: FormData vs JSON)
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      localStorage.getItem('refreshToken')
    ) {
      originalRequest._retry = true
      try {
        const { data } = await axios.post('/api/auth/refresh/', {
          refresh: localStorage.getItem('refreshToken'),
        })
        localStorage.setItem('accessToken', data.access)
        if (data.refresh) {
          localStorage.setItem('refreshToken', data.refresh)
        }
        originalRequest.headers.Authorization = `Bearer ${data.access}`
        return api(originalRequest)
      } catch {
        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default api
