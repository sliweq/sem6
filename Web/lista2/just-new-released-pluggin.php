<?php
/** 
 * Plugin Name: JustNewReleasedPluggin
 * Version: 1.1
 * Description: JustNewReleasedPluggin for Advanced Web Technologies
 * Author: Jakub Śliwka, Jan Maciuk
 * License: GPL v2 or later
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
*/

# admin panel 
function naph_admin_actions_register_menu() {
    # params: Tytuł, Nazwa/tekst wyświetlanu w menu adm, wymagane uprawnienia, url do admin panel (unique), funkcja po uruchomieniu
    add_options_page("JustNewReleasedPluggin", "JustNewReleasedPluggin", 'manage_options', "naph", "naph_admin_page");
}
add_action('admin_menu', 'naph_admin_actions_register_menu');


function naph_display_random_announcement($content) {
    $announcements = get_option('naph_announcements'); 
    if (!empty($announcements)) {
        $random_announcement = $announcements[array_rand($announcements)];
        $announcement_html = '<div class="naph-announcement">' . $random_announcement . '</div>';
        return wp_kses_post($announcement_html) . $content; 
    }

    return $content;
}
# filter (req), function name (req), priority, params 
add_filter('the_content', 'naph_display_random_announcement');



function naph_register_styles() {
    // rejestruje nasz plik styli pod nazwą z pierwszego argumentu
    wp_register_style('naph_styles', plugins_url('/css/style.css', __FILE__));
    // skazuje aby dołączyć plik zarejestrowany pod nazwą z argumentu do htmla strony.
    wp_enqueue_style('naph_styles');
}
add_action('init', 'naph_register_styles');


function naph_admin_page() {

    global $_POST;

    if (isset($_POST['naph_do_change']) ) {
        if ($_POST['naph_do_change'] == 'Y') {

            $new_announcement = $_POST['naph_announcement'];
            
            if (!empty($new_announcement)) {
                if(strlen($new_announcement) >400){
                    echo '<div class="notice notice-error is-dismissible"><p>Announcement too long.</p></div>';
                }
                else{
                    $announcements = get_option('naph_announcements', []);
                    $announcements[] = $new_announcement; 
                    
                    update_option('naph_announcements', $announcements); 
                    echo '<div class="notice notice-success is-dismissible"><p>Announcement added successfully.</p></div>';
                }
                

            }
            else{
                echo '<div class="notice notice-error is-dismissible"><p>Announcement cannot be empty.</p></div>';
            }
        }
    }

    if (isset($_POST['naph_do_edit'])) {
        $announcement_index = $_POST['announcement_index'];
        $new_announcement = $_POST['naph_announcement_edit'];

        if (!empty($new_announcement) && isset($announcement_index)) {
            $announcements = get_option('naph_announcements', []);
            if (isset($announcements[$announcement_index])) {

                $announcements[$announcement_index] = $new_announcement; 
                update_option('naph_announcements', $announcements); 
                
                echo '<div class="notice notice-success is-dismissible"><p>Announcement updated successfully.</p></div>';
            } else {
                echo '<div class="notice notice-error is-dismissible"><p>Invalid announcement index.</p></div>';
            }
        } else {
            echo '<div class="notice notice-error is-dismissible"><p>Announcement cannot be empty.</p></div>';
        }
    }

    if (isset($_POST['naph_do_delete'])) {
        $announcement_index = $_POST['announcement_index'];

        if (isset($announcement_index)) {
            $announcements = get_option('naph_announcements', []);
            if (isset($announcements[$announcement_index])) {
                unset($announcements[$announcement_index]);

                // return all values of an array
                $announcements = array_values($announcements);
                update_option('naph_announcements', $announcements);

                echo '<div class="notice notice-success is-dismissible"><p>Announcement deleted successfully.</p></div>';
            } else {
                echo '<div class="notice notice-error is-dismissible"><p>Invalid announcement index.</p></div>';
            }
        }
    }

    if (isset($_POST['cancel_edit'])) {
        unset($_POST['naph_do_edit_button']);
    }

    # [] - returned value if option do not exist
    $announcements = get_option('naph_announcements', []);
    ?>

    <div class="wrap">
        <h1>Just New Released Plugin - Manage Announcements</h1>

        <form name="naph_form" method="post">
            <input type="hidden" name="naph_do_change" value="Y">
            
            <h2>Add New Announcement</h2>
            <textarea name="naph_announcement" rows="5" cols="60" placeholder="Enter the announcement..."></textarea><br><br>
            
            <p class="submit">
                <input type="submit" value="Add">
            </p>
        </form>


        <h2>Current Announcements</h2>
        <?php if (!empty($announcements)) : ?>
            <ul>
                <?php foreach ($announcements as $index => $announcement) : ?>
                    <li>
                        <!-- filtrowanie treści i zostawia dozwolone tagi html i atrybuty, zabezpeiczba przed atakami -->
                        <?php 
                            if(strlen($announcement) > 50){
                                echo wp_kses_post(substr($announcement,0,50));
                            }
                            else {
                                echo wp_kses_post($announcement);
                            }?>
                        

                        <form method="post" style="display:inline;">
                            <input type="hidden" name="announcement_index" value="<?php echo $index; ?>">
                            <input type="submit" name="naph_do_edit_button" value="Edit">
                        </form>

                        <form method="post" style="display:inline;">
                            <input type="hidden" name="announcement_index" value="<?php echo $index; ?>">
                            <input type="submit" name="naph_do_delete" value="Delete" >
                        </form>

                        

                        <?php if (isset($_POST['naph_do_edit_button']) && $_POST['announcement_index'] == $index) : ?>
                            <form method="post" >
                                <input type="hidden" name="announcement_index" value="<?php echo $index; ?>">
                                <!--  esc_textarea- zabezpieczenie przed xxs, zabezpieczanie tekstu textarea -->
                                <textarea name="naph_announcement_edit" rows="2" cols="60"><?php echo esc_textarea($announcement); ?></textarea><br><br>
                                <input type="submit" name="naph_do_edit" value="Save">
                                <input type="submit" name="cancel_edit" value="Cancel">
                            </form>
                        <?php endif; ?>

                    </li>
                <?php endforeach; ?>
            </ul>
        <?php else : ?>
            <p>No announcements found.</p>
        <?php endif; ?>
    </div>

    <?php
}

?>
