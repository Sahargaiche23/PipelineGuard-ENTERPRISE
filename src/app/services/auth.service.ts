import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private apiUrl = 'http://localhost:8000'; // adapte selon ton backend
  private tokenKey = 'access_token';

  constructor(private http: HttpClient) {}

  login(username: string, password: string) {
    return this.http.post<{access_token: string}>(`${this.apiUrl}/login?username=${username}&password=${password}`, {});
  }

  register(username: string, password: string) {
    return this.http.post(`${this.apiUrl}/register?username=${username}&password=${password}`, {});
  }

  setToken(token: string) { localStorage.setItem(this.tokenKey, token); }
  getToken(): string | null { return localStorage.getItem(this.tokenKey); }
  logout() { localStorage.removeItem(this.tokenKey); }
  isLoggedIn(): boolean { return !!this.getToken(); }
}