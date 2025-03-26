class AddProject {
    constructor(title, genre, genre1, genre2, description) {
        this.title = title
        this.genre = genre
        this.genre1 = genre1
        this.genre = genre2
        this.description = description
    }

    async createProject()  {
        const data = JSON.stringify ({
            title: this.title,
            genre: this.genre,
            genre1: this.genre1,
            genre2: this.genre2,
            description: this.description
        });
        const options = {
            method: 'POST',
            credentials: 'include',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
              },
            body: data
        };
        try {
            console.log('Fetch request starting...');
            const response = await fetch('http://localhost:5000/add_project', options);
            if (!response.ok) {
                const err = await response.json();
                console.log("Is this working?");
                throw new Error (err.error);
            }
            const data = await response.json();
            if (data.success) {
                window.location.href = '/user_home';
            } 
        } catch (error) {
            console.error('Error:', error.message);
        }
    }
}

const titleInput = document.querySelector('input[name="title"]');
const genreInput = document.querySelector('input[name="genre"]');
const genre1Input = document.querySelector('input[name="genre1"]');
const genre2Input = document.querySelector('input[name="genre2"]');
const descriptionInput = document.querySelector('input[name="description"]');

if (document.getElementById('submit')) {
    document.getElementById('submit').addEventListener('click', (event) => {
        if (!titleInput.value) {
            document.getElementById("error").innerHTML = "Please enter at least a title.";
        } else {
            event.preventDefault();
            const projectInstance = new AddProject(titleInput.value, genreInput.value, genre1Input.value, genre2Input.value, descriptionInput.value,);
        
            projectInstance.createProject();
        }
    });
    
}
