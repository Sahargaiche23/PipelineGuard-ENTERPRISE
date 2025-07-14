// src/app/login/login.component.ts
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  error: string = '';
  showPassword: boolean = false;
  rememberMe: boolean = false;

  constructor(private authService: AuthService, private router: Router) {}

  togglePasswordVisibility(): void {
    this.showPassword = !this.showPassword;
  }

  login() {
    this.error = ''; // Clear previous errors
    
    console.log('🔐 Tentative de connexion pour:', this.username);
    
    this.authService.login(this.username, this.password).subscribe({
      next: (response: any) => {
        console.log('✅ Connexion réussie:', response);
        this.authService.setToken(response.access_token);
        this.router.navigate(['/notifications']);
      },
      error: (error) => {
        console.error('❌ Erreur de connexion:', error);
        if (error.status === 401) {
          this.error = 'Nom d\'utilisateur ou mot de passe incorrect';
        } else if (error.status === 0) {
          this.error = 'Impossible de se connecter au serveur. Vérifiez votre connexion.';
        } else {
          this.error = 'Une erreur s\'est produite lors de la connexion';
        }
      }
    });
  }
}
