FROM osgeo/grass-gis:main-alpine

ARG ADDON_NAME
ARG GITHUB_REPOSITORY

WORKDIR /src
COPY . /src

RUN apk add gcc make python3-dev
# musl-dev linux-headers

# create environment to install requirements
RUN python -m venv addon-env
# RUN source addon-env/bin/activate
ENV PATH="/src/addon-env/bin:$PATH"
RUN test -e requirements.txt && pip3 install -r requirements.txt || echo "No requirements.txt"

# Compile GRASS GIS addon
RUN grass --tmp-location XY --exec g.extension extension=${ADDON_NAME} url=. prefix=build --verbose
RUN mv build/docs/html/${ADDON_NAME}.html build/docs/html/index.html

# Reset URL
RUN sed -i "s+file:///usr/local/grass84/docs/html/+https://grass.osgeo.org/grass-stable/manuals/+g" build/docs/html/index.html
RUN sed -i "s+(<a href=\"\">history</a>)+(<a href=\"https://github.com/${GITHUB_REPOSITORY}/commits/main/\">history</a>)+g" build/docs/html/index.html
RUN sed -i "s+<a href=\"\">+<a href=\"https://github.com/${GITHUB_REPOSITORY}\">+g" build/docs/html/index.html

# RUN deactivate