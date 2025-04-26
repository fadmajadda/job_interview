export default {
  name: 'App',
  data() {
    return {
      jobDescription: '',
      questionCount: 15, // Valeur par défaut
      questionFormat: 'qcm', // Nouvelle propriété
      questions: [],       // Liste de toutes les questions générées
      currentQuestionIndex: 0, // Index de la question actuelle
      selectedOption: null,
      answerChecked: false,
      isLoading: false,
      error: null,
      techData: null,
      userAnswer: '', // Manquant
    isAnswerCorrect: false, // Manquant
    answerScore: 0, // Manquant
    answerFeedback: '', // Manquant
    isCheckingAnswer: false // Manquant
    }
  },
  computed: {
    currentQuestion() {
      return this.questions[this.currentQuestionIndex] || null;
    },
    progress() {
      return this.questions.length > 0 
        ? Math.round((this.currentQuestionIndex + 1) / this.questions.length * 100)
        : 0;
    },
    isFirstQuestion() {
      return this.currentQuestionIndex === 0;
    },
    isLastQuestion() {
      return this.currentQuestionIndex === this.questions.length - 1;
    }
  },
  methods: {
    async generateQuestions() {
      if (!this.jobDescription.trim()) {
        this.error = "Veuillez entrer une offre d'emploi";
        return;
      }
      if (this.questionCount < 5 || this.questionCount > 30) {
        this.error = "Veuillez entrer un nombre entre 5 et 30";
        return;
      }
      this.isLoading = true;
      this.error = null;
      this.questions = [];
      this.currentQuestionIndex = 0;
      
      try {
        const response = await fetch('http://localhost:5000/generate_questions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            job_description: this.jobDescription,
            question_count: this.questionCount,
            question_format: this.questionFormat // Nouveau paramètre
          })
        });
        
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.message || 'Erreur lors de la génération des questions');
        }
        
        const data = await response.json();
        // Randomisation des options pour chaque question
        // Ne randomisez les réponses que pour le format QCM
    this.questions = this.questionFormat === 'qcm' 
    ? this.randomizeCorrectAnswers(data.questions) 
    : data.questions;
        this.techData = data.tech_data;
        this.resetQuestionState();
        
      } catch (err) {
        this.error = err.message || 'Une erreur est survenue';
        console.error('API Error:', err);
      } finally {
        this.isLoading = false;
      }
    },
    async validateAnswer() {
      if (!this.userAnswer.trim()) return;
      
      this.isCheckingAnswer = true;
      
      try {
        const response = await fetch('http://localhost:5000/validate_answer', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            question: this.currentQuestion,
            user_answer: this.userAnswer
          })
        });
    
        if (!response.ok) {
          throw new Error('Erreur lors de la validation');
        }
    
        const result = await response.json();
        
        this.isAnswerCorrect = result.is_correct;
        this.answerScore = result.score;
        this.answerFeedback = result.feedback || result.explanation; // Selon ce que retourne votre API
        this.answerChecked = true;
    
      } catch (error) {
        console.error("Validation error:", error);
        this.isAnswerCorrect = false;
        this.answerFeedback = "Erreur lors de la validation";
        this.answerScore = 0;
      } finally {
        this.isCheckingAnswer = false;
      }
    },
    randomizeCorrectAnswers(questions) {
      return questions.map(question => {
        // Trouve l'option correcte
        const correctOption = question.options.find(opt => opt.correct);
        const incorrectOptions = question.options.filter(opt => !opt.correct);
        
        // Mélange les options incorrectes
        this.shuffleArray(incorrectOptions);
        
        // Choisit une position aléatoire pour la bonne réponse (0 à 4)
        const correctPosition = Math.floor(Math.random() * 5);
        
        // Reconstruit le tableau d'options
        const randomizedOptions = [
          ...incorrectOptions.slice(0, correctPosition),
          correctOption,
          ...incorrectOptions.slice(correctPosition)
        ];
        
        return {
          ...question,
          options: randomizedOptions
        };
      });
    },
    // Fonction pour mélanger un tableau (algorithme Fisher-Yates)
    shuffleArray(array) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
      return array;
    },
    checkAnswer() {
      if (this.selectedOption !== null) {
        this.answerChecked = true;
        this.scrollToExplanation();
      }
    },
    nextQuestion() {
      if (!this.isLastQuestion) {
        this.currentQuestionIndex++;
        this.resetQuestionState();
      }
    },
    prevQuestion() {
      if (!this.isFirstQuestion) {
        this.currentQuestionIndex--;
        this.resetQuestionState();
      }
    },
    resetQuestionState() {
      this.selectedOption = null;
      this.userAnswer = ''; // À ajouter
      this.answerChecked = false;
      this.isAnswerCorrect = false; // À ajouter
      this.answerScore = 0; // À ajouter
      this.answerFeedback = ''; // À ajouter
      this.isCheckingAnswer = false; // À ajouter
      this.scrollToTop();
    },
    resetQuiz() {
      this.questions = [];
      this.currentQuestionIndex = 0;
      this.resetQuestionState();
    },
    scrollToExplanation() {
      this.$nextTick(() => {
        const explanation = document.querySelector('.explanation');
        if (explanation) {
          explanation.scrollIntoView({ behavior: 'smooth' });
        }
      });
    },
    showAnswer() {
      this.answerChecked = true;
      this.scrollToExplanation();
    },
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }
}