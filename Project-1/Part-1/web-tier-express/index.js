const fs = require("fs");
const path = require("path");
const express = require("express");
const cors = require("cors");
const multer = require("multer");

const logger = require("./utils/logger")(module);

const app = express();
const upload = multer({});

app.use(cors());
app.disable("x-powered-by");

// Data loading
const fastCSV = require("fast-csv");
let lookup = [];
fs.createReadStream(path.resolve(__dirname, "data", "results.csv"))
	.pipe(fastCSV.parse({ headers: true }))
	.on('error', error => console.error(error))
	.on('data', row => lookup.push(row))
	.on('end', (rowCount) => console.log(`Parsed ${rowCount} rows`));

// Controllers

const imageRecognition = (req, res, next) => {
	try {
		const fileName = req.files.inputFile[0].originalname.split(".jpg")[0];
		return res.status(200).send(
			fileName + ":" + lookup.filter((row) => row["Image"] === fileName)[0]["Results"]
		);
	} catch (error) {
		logger.error("imageRecognition", { error });
		return res.status(500).send({ message: "Server Error. Try again." });
	}
};

// Routes
app.post("/", upload.fields([
	{ name: "inputFile", maxCount: 1 },
]), imageRecognition);

app.use((_req, res) => {
	return res.status(200).send("Web tier on ExpressJS.");
});

const port = process.env.PORT || 5000;

app.listen(port, () => {
	logger.info(`App Listening on port ${port}`);
});
