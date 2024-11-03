from lmdeploy import pipeline, TurbomindEngineConfig
from lmdeploy.vl import load_image
import pathlib
import time

current_folder = pathlib.Path(__file__).parent
images_folder = current_folder / "images"

# get all image paths
image_paths = []
for image_path in images_folder.iterdir():
    image_paths.append(image_path.resolve().as_posix())

model = "OpenGVLab/InternVL2-2B"
pipe = pipeline(model, backend_config=TurbomindEngineConfig(session_len=8192))

start_time = time.time()
for path in image_paths:
    image = load_image(path)
    response = pipe(("what is the meaning of this image", image))
    print(response.text)
end_time = time.time()

elapsed_time = end_time - start_time
print(f"Time taken: {elapsed_time:.2f} seconds")


# The image is a humorous meme that plays on the common phrase "Password Incorrect" to create a comical situation. The meme uses a cat with glasses to represent the user, and it humorously illustrates the consequences of entering the wrong password. Here's a breakdown of the humor:

# 1. **First Row:**
#    - The text reads: "Password Incorrect"
#    - The cat is shown with a confused expression, looking at the screen.
#    - The text below reads: "*Resets password*"

# 2. **Second Row:**
#    - The text reads: "Password Incorrect"
#    - The cat is shown with a surprised or confused expression, looking at the screen.
#    - The text below reads: "Your password cannot be your previous password"

# 3. **Third Row:**
#    - The text reads: "Your password cannot be your previous password"
#    - The cat is shown with a shocked or confused expression, looking at the screen.
#    - The text below reads: "*Resets password*"

# The humor arises from the absurdity of the situation: the cat, with glasses, is shown as if it is trying to enter a password, but the cat's expression and the text below indicate that it is resetting the password. This creates a comical effect by exaggerating the user's mistake and the cat's reaction.


# The image depicts a comparison of Earth before and after a person's opinion. The text above the images reads, "A picture of earth before and after your opinion." This suggests that the Earth's appearance or state is being presented as a result of the individual's perspective or viewpoint.

# ### Detailed Analysis:

# 1. **Before Opinion**:
#    - The left side of the image shows Earth as it was before any significant human influence or opinion was applied. This includes the natural state of the planet, with its recognizable continents, oceans, and atmosphere.
#    - The right side of the image shows Earth after the individual's opinion has been applied. This includes the altered appearance of the continents, the altered coloration of the oceans, and the overall altered state of the planet.

# 2. **Implications of the Image**:
#    - **Global Changes**: The image highlights the significant impact of human activities on the Earth. The alterations seen on both sides of the image reflect the effects of climate change, pollution, deforestation, and other environmental issues.
#    - **Ecosystem Disruption**: The changes in the appearance of the continents and oceans suggest disruptions in the natural ecosystems, such as the melting of polar ice caps, rising sea levels, and changes in ocean currents.
#    - **Human Impact**: The alterations in the Earth's appearance also reflect the impact of human activities on the environment. This includes the burning of fossil fuels, deforestation, and industrial pollution.

# ### Conclusion:
# The image serves as a powerful visual metaphor for the profound and far-reaching effects of human actions on the planet. It underscores the need for collective action to address environmental issues and the importance of considering the perspectives of all stakeholders in the effort to protect our planet.
# The image contains a humorous meme that plays on the idea of college education and job qualifications. The text reads:


# "forget everything you learned in college, you won't need it working here"
# "but, I didn't go to college"

# The punchline is:

# "well then, you're unqualified for this job"

# The meme humorously suggests that even if one did not attend college, they are still not qualified for the job in question. The cat in the image, with its starburst mark, adds a comical element to the joke, as it appears to be looking at the text with a puzzled or confused expression.
