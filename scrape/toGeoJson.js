const fs = require('fs');

const featureCollection = {
    type: "FeatureCollection",
    features: [],
}

fs.readFile("pairs.json", async (err, data) => {
    console.log(data);
    const string = await data.toString();
    const pythonList = JSON.parse(string);
    // {title: __, lat: __, lng: __}
    pythonList.forEach(entry => {
        const pointGeometry = {
            type: "Feature",
            properties: {
                name: entry.title
            },
            geometry: {
                type: "Point",
                coordinates: [
                    parseFloat(entry.lng),
                    parseFloat(entry.lat),
                ],
            },
        };
        featureCollection.features.push(pointGeometry);
    });
    fs.writeFile("geo1.json", JSON.stringify(featureCollection), console.error);
})