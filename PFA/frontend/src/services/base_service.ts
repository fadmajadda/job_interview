import axios from "axios";


const Api = () => {

    return axios.create({
        baseURL: 'http://localhost:5000/generate_questions',
        timeout: 180000,
        withCredentials: true,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
    });

}

export default Api;