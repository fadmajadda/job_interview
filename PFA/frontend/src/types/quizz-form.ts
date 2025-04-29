export type QuestionFormatType = 'qcm' | 'qa'



export interface QuestionForm {
    job_description:string;
    question_count:string;
    question_format:string;
}