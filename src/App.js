/*
 * Copyright 2025 Sherwin Allen, Shambo Sarkar, Sathvik S, Meeran Ahmed
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
// App.js
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import IoTExtractor from './components/IoTExtractor';
import DevicePage from './components/DevicePage';
import LoginPage from './components/LoginPage'
import CaseInfo from './components/CaseInformation'
import FileSystem from './components/FileSystem'
import SmartWatch from './components/SmartWatch';

const App = () => (
  <Router>
    <Routes>
      <Route path="/" element={<IoTExtractor/>} />
      <Route path="/caseinfo" element={<CaseInfo />} />
      <Route path="/iotextractor" element={<IoTExtractor />} />
      <Route path="/:deviceName" element={<DevicePage />} />
      <Route path="/filesystem" element={<FileSystem/>}/>
      <Route path="/smartwatch" element={<SmartWatch/>}/>
    </Routes>
  </Router>
);

export default App;