import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { NotificationService } from 'src/app/services/notification.service';
import { AuthService } from 'src/app/services/auth.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit, OnDestroy {
  notificationCount = 0;
  isUserMenuOpen = false;
  currentUser: any = null;
  private notifSub?: Subscription;

  constructor(
    private notificationService: NotificationService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Récupérer les informations utilisateur
    this.loadCurrentUser();
    
    // Écouter les notifications
    this.notifSub = this.notificationService.notifications$.subscribe(() => {
      this.notificationCount++;
    });

    // Fermer le menu utilisateur au clic extérieur
    document.addEventListener('click', this.handleClickOutside.bind(this));
  }

  ngOnDestroy(): void {
    this.notifSub?.unsubscribe();
    document.removeEventListener('click', this.handleClickOutside.bind(this));
  }

  loadCurrentUser(): void {
    // Simuler les données utilisateur - à remplacer par un vrai service
    const token = this.authService.getToken();
    if (token) {
      try {
        // Décoder le token JWT pour obtenir le nom d'utilisateur
        const payload = JSON.parse(atob(token.split('.')[1]));
        this.currentUser = {
          username: payload.sub || 'Utilisateur',
          email: 'admin@pipelineguard.com',
          role: 'Admin'
        };
      } catch (error) {
        console.error('Erreur lors du décodage du token:', error);
        this.currentUser = { username: 'Utilisateur', role: 'Admin' };
      }
    }
  }

  toggleUserMenu(): void {
    this.isUserMenuOpen = !this.isUserMenuOpen;
  }

  closeUserMenu(): void {
    this.isUserMenuOpen = false;
  }

  navigateToNotifications(): void {
    this.router.navigate(['/notifications']);
  }

  logout(event: Event): void {
    event.preventDefault();
    event.stopPropagation();
    
    // Confirmation de déconnexion
    if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
      this.authService.logout();
      this.notificationService.close();
      this.closeUserMenu();
      this.router.navigate(['/login']);
    }
  }

  private handleClickOutside(event: Event): void {
    const target = event.target as HTMLElement;
    const userProfile = document.querySelector('.user-profile');
    const userDropdown = document.querySelector('.user-dropdown');
    
    if (userProfile && userDropdown && 
        !userProfile.contains(target) && 
        !userDropdown.contains(target)) {
      this.closeUserMenu();
    }
  }
}
