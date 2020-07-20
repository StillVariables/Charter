const colors = require('colors/safe');
const ConfigError = require('./config-error');
const clipboardy = require('clipboardy');
const config = require('./config.json');
const {waitForClipboardStartingWith} = require('./clipboard-utils');
const {
	retrieveAccessToken,
	createAccountAccessConsent,
	authoriseProgramatically,
	authoriseManually,
	getAccounts,
	getDetails
} = require('./api');

const http = require('http');

const hostname = '127.0.0.1';
const port = 3000;
const mydata = '';

authoriseAndGetAccounts(process.argv[2] === 'manual');

async function authoriseAndGetAccounts(manualAuthorisation = false) {
	try {
		console.log('Getting initial access token...');
		const accessToken = await retrieveAccessToken();

		console.log(`Access Token: ${format(accessToken)}. Creating consent...`);
		const consentId = await createAccountAccessConsent(accessToken);

		console.log(`Consent ID: ${format(consentId)}. Authorising...`);
		const authorisationCode = manualAuthorisation
			? await startManualAuthorisation(consentId)
			: await authoriseProgramatically(consentId);

		console.log(`Authorisation code received: ${format(authorisationCode)}. Retrieving authorised access token...`);
		const authorisedAccessToken = await retrieveAccessToken(authorisationCode);

		console.log(`Access Token: ${format(authorisedAccessToken)}. Retrieving users accounts...`);
		//const accounts = await getAccounts(authorisedAccessToken);
		console.log(`Access Token: ${format(authorisedAccessToken)}. Retrieving account details...`);
		//const ddata = await getDetails(authorisedAccessToken);

		//console.log('Accounts:');
		//console.log(JSON.stringify(ddata, null, 4));

		const server = http.createServer(async (req, res) => {
			res.statusCode = 200;
			res.setHeader('Content-Type', 'text/plain');
			var url = req.url;
			if(url == '/accounts')
			{
				const accounts = await getAccounts(authorisedAccessToken);
				//res.end('heheh');	
				res.end(JSON.stringify(accounts, null, 4));	
			}
			if(url == '/balance')
			{
				const ddata = await getDetails(authorisedAccessToken);
				res.end(JSON.stringify(ddata, null, 4));
			}
			
		  });
		  
		  server.listen(port, hostname, () => {
			console.log(`Server running at http://${hostname}:${port}/`);
		  });
		  

	} catch (error) {
		if (error instanceof ConfigError)
			console.log('Configuration error: ', error.message);
		else
			throw error;
	}
}

async function startManualAuthorisation(consentId) {
	return await authoriseManually(consentId, async userAuthorisationUrl => {
		await clipboardy.write(userAuthorisationUrl);

		console.log();
		console.log('Url for manual authorisation copied to clipboard, launch in a browser to proceed.');
		console.log('Once complete, copy the redirected URL to continue...');
		console.log();

		return await waitForClipboardStartingWith(`http://${config.teamDomain}/redirect`);
	});
}

function format(item) {
	return colors.magenta(item.length > 50
		? (item.substring(0, 50) + '…')
		: item);
}