const SPREADSHEET_ID = '1DyX14qtc1FvTacYi_doZmOvAxoZ3dciQZbUM4CVjnSU';
const USER_ROLES = ['Admin', 'Donor', 'Requester'];

/**
 * Entry point for WebApp
 */
function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('LifeLink Blood Portal');
}

/**
 * Get Google Sheet by name
 */
function getSheet(name) {
  try {
    return SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName(name);
  } catch(e) {
    throw new Error(`Error accessing sheet ${name}: ${e.message}`);
  }
}

/**
 * Sanitize inputs by removing HTML tags and trimming whitespace
 */
function sanitize(input) {
  if (!input) return '';
  return String(input).trim()
    .replace(/<[^>]*>?/gm, '')  // remove HTML tags
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

/**
 * Validate user role exists
 */
function isValidRole(role) {
  return USER_ROLES.includes(role);
}

/**
 * Register donor with validation and sanitization
 */
function registerDonor(name, phone, bloodGroup, city) {
  name = sanitize(name);
  phone = sanitize(phone);
  bloodGroup = sanitize(bloodGroup);
  city = sanitize(city);
  
  if (![name, phone, bloodGroup, city].every(v => v.length > 0)) {
    return 'All donor fields are required.';
  }
  if (!/^(\+?\d{10,15})$/.test(phone)) {
    return 'Invalid phone format.';
  }

  const sheet = getSheet('Donors');
  if (!sheet) return 'Donors sheet missing';

  const data = sheet.getDataRange().getValues();
  if (data.some(row => row[2] === phone)) {
    return 'Donor with this phone already exists.';
  }

  sheet.appendRow([new Date(), name, phone, bloodGroup, city]);
  return 'success';
}

/**
 * Register blood request with validation and sanitization
 */
function registerRequest(name, phone, bloodGroup, city) {
  name = sanitize(name);
  phone = sanitize(phone);
  bloodGroup = sanitize(bloodGroup);
  city = sanitize(city);
  
  if (![name, phone, bloodGroup, city].every(v => v.length > 0)) {
    return 'All request fields are required.';
  }
  if (!/^(\+?\d{10,15})$/.test(phone)) {
    return 'Invalid phone format.';
  }

  const sheet = getSheet('Requests');
  if (!sheet) return 'Requests sheet missing';

  sheet.appendRow([new Date(), name, phone, bloodGroup, city]);
  return 'success';
}

/**
 * Get current blood stock levels from BloodStock sheet
 */
function getBloodStock() {
  const sheet = getSheet('BloodStock');
  if (!sheet) return [];
  const data = sheet.getDataRange().getValues();
  data.shift(); // skip headers
  return data.map(row => ({ bloodGroup: row[0], units: Number(row[1]) || 0 }));
}

/**
 * Dashboard stats with real-time updates
 * Role can be used for permission gating (currently open but can restrict)
 */
function getDashboardStats(role) {
  if (!isValidRole(role)) throw new Error('Unauthorized');

  const donorsSheet = getSheet('Donors');
  const requestsSheet = getSheet('Requests');
  const bloodStock = getBloodStock();

  return {
    totalDonors: donorsSheet ? donorsSheet.getLastRow() - 1 : 0,
    totalRequests: requestsSheet ? requestsSheet.getLastRow() - 1 : 0,
    bloodStock
  };
}

/**
 * Donor search with pagination, admin-only
 * filterTerm: search string; page, pageSize: paging
 */
function searchDonors(filterTerm, page = 1, pageSize = 5, role = 'Donor') {
  if (role !== 'Admin') throw new Error('Access denied');

  filterTerm = sanitize(filterTerm).toLowerCase();
  const sheet = getSheet('Donors');
  if (!sheet) return { items: [], total: 0 };

  const data = sheet.getDataRange().getValues();
  data.shift(); // remove headers

  let filtered = data;
  if (filterTerm) {
    filtered = data.filter(row => {
      return row[1].toLowerCase().includes(filterTerm) || 
             row[3].toLowerCase().includes(filterTerm) || 
             row[4].toLowerCase().includes(filterTerm);
    });
  }

  const total = filtered.length;
  const start = (page - 1) * pageSize;
  const items = filtered.slice(start, start + pageSize);

  return { items, total };
}
function hash(str) {
  // Simple hash for demo ONLY. Use proper hash in production!
  return Utilities.base64Encode(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, str));
}

function registerUser(name, email, password, role) {
  name = sanitize(name);
  email = sanitize(email);
  password = sanitize(password);
  role = sanitize(role);

  var sheet = getSheet('Users');
  if (!sheet) return 'Users sheet missing';

  // Check if user exists
  var data = sheet.getDataRange().getValues();
  if (data.some(row => row[2] === email)) {
    return 'User with this email already exists.';
  }
  // Add row
  sheet.appendRow([new Date(), name, email, hash(password), role]);
  return 'success';
}

function loginUser(email, password) {
  email = sanitize(email);
  password = sanitize(password);

  var sheet = getSheet('Users');
  if (!sheet) return 'Users sheet missing';
  
  var data = sheet.getDataRange().getValues();
  var found = data.find(row => row[2] === email && row[3] === hash(password));
  if (found) return { success: true, role: found[4], name: found[1] };
  else return { success: false };
}
function doGet(e) {
  var page = e.parameter.page;
  if (!page || page === 'index') {
    return HtmlService.createTemplateFromFile('Index').evaluate();
  } else if (page === 'about') {
    return HtmlService.createTemplateFromFile('About').evaluate();
  } else if (page === 'terms') {
    return HtmlService.createTemplateFromFile('Terms').evaluate();
  } 
  // Add else if conditions for other pages similarly
  else {
    return HtmlService.createTemplateFromFile('Index').evaluate(); // default to home
  }
}
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}

