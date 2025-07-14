import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  username = '';
  email = '';
  password = '';
  confirmPassword = '';
  acceptTerms = false;
  showPassword = false;
  showConfirmPassword = false;
  isLoading = false;
  errorMessage = '';
  successMessage = '';

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  get passwordMismatch(): boolean {
    return this.password !== this.confirmPassword && this.confirmPassword.length > 0;
  }

  togglePasswordVisibility(): void {
    this.showPassword = !this.showPassword;
  }

  toggleConfirmPasswordVisibility(): void {
    this.showConfirmPassword = !this.showConfirmPassword;
  }

  register(): void {
    if (this.passwordMismatch) {
      this.errorMessage = 'Les mots de passe ne correspondent pas';
      return;
    }

    if (!this.acceptTerms) {
      this.errorMessage = 'Vous devez accepter les conditions d\'utilisation';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';

    console.log('🚀 Tentative d\'inscription pour:', this.username);

    // Appel au service d'authentification
    this.authService.register(this.username, this.password).subscribe({
      next: (response) => {
        console.log('✅ Inscription réussie:', response);
        this.successMessage = 'Compte créé avec succès ! Connexion automatique...';
        
        // Connexion automatique après inscription réussie
        this.loginAfterRegister();
      },
      error: (error) => {
        console.error('❌ Erreur lors de l\'inscription:', error);
        this.isLoading = false;
        
        if (error.status === 400) {
          this.errorMessage = 'Ce nom d\'utilisateur existe déjà';
        } else if (error.status === 422) {
          this.errorMessage = 'Données invalides. Vérifiez vos informations.';
        } else if (error.status === 0) {
          this.errorMessage = 'Impossible de se connecter au serveur. Vérifiez votre connexion.';
        } else {
          this.errorMessage = 'Une erreur s\'est produite. Veuillez réessayer.';
        }
      }
    });
  }

  private loginAfterRegister(): void {
    console.log('🔑 Connexion automatique après inscription...');
    
    this.authService.login(this.username, this.password).subscribe({
      next: (response) => {
        console.log('✅ Connexion automatique réussie:', response);
        this.authService.setToken(response.access_token);
        this.isLoading = false;
        this.successMessage = 'Inscription et connexion réussies ! Redirection...';
        
        // Redirection vers les notifications après 1.5 secondes
        setTimeout(() => {
          this.router.navigate(['/notifications']);
        }, 1500);
      },
      error: (error) => {
        console.error('❌ Erreur lors de la connexion automatique:', error);
        this.isLoading = false;
        this.successMessage = 'Inscription réussie ! Redirection vers la connexion...';
        
        // Si la connexion automatique échoue, rediriger vers login
        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 2000);
      }
    });
  }
}
