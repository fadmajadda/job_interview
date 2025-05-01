import {QuestionForm} from "@/types/quizz-form.js";
import Api from "@/services/base_service.js";
import {endpoints} from "@/services/endpoints.js";


const generateQuizzQuestions = async (form: QuestionForm) => {
    try {
        return await Api().post(endpoints.GENERATE_QUESTIONS, form);
    } catch (err) {
       // Transforme les erreurs Axios en erreurs lisibles
         throw new Error(err.response?.data?.message || "Échec de la génération des questions");
    }
}


export {
    generateQuizzQuestions
}