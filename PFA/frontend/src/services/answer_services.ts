import { AnswerFrom } from "@/types/answer_from.ts";
import Api from "@/services/base_service.ts";
import { endpoints } from "@/services/endpoints.ts";

const validate_answer = async (form: AnswerFrom) => {
    try {
        const response = await Api().post(endpoints.VALIDATE_ANSWER, form);
        return response;
    } catch (err) {
        throw new Error(err.response?.data?.message || "Échec de la validation de la réponse");
    }
}

export { validate_answer };