fetch('http://localhost:5000/login', options)
            .then(response => {
                // Check if the request was successful
                if (!response.ok) {
                    throw new Error ('Network response was not ok');
                }
                return response.json();
            })
            .then(responseData => {
                if (responseData.success) {
                    window.location.href = '/user_home';
                }
                else {
                    alert('Login failed: ' + responseData.error);
                    }
                })
            .catch(error => {
                    console.error('Fetch error:', error);
                });

<form method="post">
            <input type="image" src="static\book2.png" alt="book.png" width=10% height="10%">
            <figure id="project">Project</figure>